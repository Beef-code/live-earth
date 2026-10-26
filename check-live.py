#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-live.py — 复核每个机位是不是真的还在直播。

用法:  python check-live.py [index.html]

为什么需要它：YouTube 直播每次主播重启就换 ID，旧 ID 变成"已结束"，机位点开就是死 iframe。
validate.js 只查结构，查不出这个，必须联网。

判活方法（踩过的坑都写在 README 里了）：
  * YouTube（直播）—— 用 innertube player 接口读 videoDetails.isLive
      - 不要爬 watch 页面：几十次请求后会返回 reCAPTCHA 页，静默变成假死
      - 不要用 maxresdefault_live.jpg：已结束的直播也返回 200
  * YouTube（步行漫游，walk:true）—— 是录播，没有直播状态，只查 oEmbed 是否 200（可公开嵌入）
  * Bilibili —— room/v1/Room/get_info 的 live_status == 1，并且 keyframe 不带 Referer 也能取到
  * 其他 —— 直接 HEAD 源地址

退出码 0 = 全部正常，1 = 有失效机位。
"""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
CV = "2.20241010.01.00"
PATH = sys.argv[1] if len(sys.argv) > 1 else "index.html"


def curl(args):
    return subprocess.run(["curl", "-s", "-L", "--max-time", "25"] + args,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def http_code(url):
    return subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                           "--max-time", "20", url, "-H", "User-Agent: " + UA],
                          capture_output=True, text=True).stdout.strip()


def yt_is_live(vid):
    """True / False / None（拿不到）"""
    body = json.dumps({"context": {"client": {"clientName": "WEB", "clientVersion": CV,
                                              "hl": "en", "gl": "US"}},
                       "videoId": vid})
    out = curl(["https://www.youtube.com/youtubei/v1/player?prettyPrint=false",
                "-H", "Content-Type: application/json",
                "-H", "User-Agent: " + UA,
                "-H", "X-Youtube-Client-Name: 1",
                "-H", "X-Youtube-Client-Version: " + CV,
                "--data-binary", body])
    try:
        d = json.loads(out)
    except Exception:
        return None, ""
    vd = d.get("videoDetails") or {}
    return vd.get("isLive") is True, vd.get("title", "")


def yt_embeddable(vid):
    return http_code("https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=%s&format=json" % vid)


def bili_live(rid):
    out = curl(["https://api.live.bilibili.com/room/v1/Room/get_info?room_id=%s" % rid,
                "-H", "User-Agent: " + UA, "-H", "Referer: https://live.bilibili.com/"])
    try:
        d = json.loads(out).get("data") or {}
    except Exception:
        return False, "api-error"
    if d.get("live_status") != 1:
        return False, "offline"
    kf = d.get("keyframe") or ""
    if kf and not http_code(kf).startswith("2"):
        return False, "keyframe " + http_code(kf)
    return True, "ok"


def check(cam):
    name = cam.get("name", "?")
    if cam.get("walk"):
        # 步行漫游是录播，没有直播状态可查，只看是否还能公开嵌入
        code = yt_embeddable(cam["yt"])
        if code == "200":
            return ("VOD", name, cam["yt"], "步行漫游录播 · 可嵌")
        return ("DEAD", name, cam["yt"], "oEmbed " + code)
    if cam.get("yt"):
        live, title = yt_is_live(cam["yt"])
        if live is None:
            return ("UNKNOWN", name, cam["yt"], "接口无响应")
        if not live:
            return ("DEAD", name, cam["yt"], title[:60])
        if yt_embeddable(cam["yt"]) != "200":
            return ("BLOCKED", name, cam["yt"], title[:60])
        return ("LIVE", name, cam["yt"], title[:60])
    if cam.get("bili"):
        ok, why = bili_live(cam["bili"])
        return ("LIVE" if ok else "DEAD", name, "bili:" + str(cam["bili"]), why)
    if cam.get("api") or cam.get("type") == "sgapi":
        return ("LIVE", name, "api", "开放 API，跳过")
    src = cam.get("src") or ""
    if not src:
        return ("DEAD", name, "-", "没有任何源")
    code = http_code(src)
    return ("LIVE" if code.startswith("2") else "DEAD", name, src[:56], code)


def main():
    html = open(PATH, encoding="utf-8").read()
    a = html.index("const CAMS = [")
    b = html.index("];", a)
    # 这是 JS 对象字面量，Python 解析不了，所以按花括号配对切出每个对象再取字段
    block = html[a:b]
    objs = []
    for m in re.finditer(r'\{name:"', block):
        start = m.start()
        depth, i, in_str, q = 0, start, False, ""
        while i < len(block):
            ch = block[i]
            if in_str:
                if ch == "\\":
                    i += 2
                    continue
                if ch == q:
                    in_str = False
            else:
                if ch in "\"'":
                    in_str, q = True, ch
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        break
            i += 1
        objs.append(block[start:i + 1])

    def field(o, k):
        m = re.search(k + r':"([^"]*)"', o)
        return m.group(1) if m else None

    def numfield(o, k):
        m = re.search(k + r":(\d+)", o)
        return m.group(1) if m else None

    parsed = []
    for o in objs:
        parsed.append({"name": field(o, "name"), "yt": field(o, "yt"),
                       "bili": numfield(o, "bili"), "src": field(o, "src"),
                       "api": field(o, "api"), "type": field(o, "type"),
                       "walk": "walk:true" in o})

    print("共 %d 个机位，开始联网复核…\n" % len(parsed))
    rows = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, r in enumerate(ex.map(check, parsed), 1):
            rows.append(r)
            if i % 25 == 0:
                print("  %d/%d" % (i, len(parsed)), file=sys.stderr)

    from collections import Counter
    print("\n=== 结果 ===")
    for k, v in Counter(r[0] for r in rows).most_common():
        print("  %-8s %d" % (k, v))

    bad = [r for r in rows if r[0] in ("DEAD", "UNKNOWN")]
    if bad:
        print("\n=== 需要处理 ===")
        for st, name, sid, why in bad:
            print("  [%s] %-30s %-58s %s" % (st, name, sid, why))
        print("\n直播 ID 会过期。换 ID 的办法见 README 的 Known limitations。")
        return 1
    print("\n全部机位正常：直播都在播，漫游录播都还能嵌。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
