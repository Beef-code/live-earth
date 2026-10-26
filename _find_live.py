# -*- coding: utf-8 -*-
"""用 innertube 搜索 + player 双重校验，找指定地点的真实直播。
用法: python _find_live.py "antarctica live cam"
"""
import sys, json, re, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
CTX = {"context": {"client": {"clientName": "WEB", "clientVersion": "2.20241010.01.00"}}}


def post(url, body):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA,
                 "Accept-Language": "en-US,en;q=0.9"},
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def search_live(q):
    """sp=EgJAAQ%3D%3D 是 YouTube 的 'Live now' 过滤器"""
    body = dict(CTX)
    body.update({"query": q})
    d = post("https://www.youtube.com/youtubei/v1/search?prettyPrint=false", body)
    out = []

    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                vid = v.get("videoId")
                title = ""
                try:
                    title = "".join(r.get("text", "") for r in v["title"]["runs"])
                except Exception:
                    title = v.get("title", {}).get("simpleText", "")
                ch = ""
                try:
                    ch = v["ownerText"]["runs"][0]["text"]
                except Exception:
                    pass
                badge = ""
                try:
                    badge = "".join(r.get("text", "") for r in v["badges"][0]["metadataBadgeRenderer"].get("label", ""))
                except Exception:
                    badge = str(v.get("badges", ""))[:0]
                if vid:
                    out.append({"id": vid, "title": title, "channel": ch, "badge": badge})
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(d)
    seen, uniq = set(), []
    for v in out:
        if v["id"] in seen:
            continue
        seen.add(v["id"])
        uniq.append(v)
    return uniq


def check(vid):
    body = dict(CTX)
    body["videoId"] = vid
    try:
        d = post("https://www.youtube.com/youtubei/v1/player?prettyPrint=false", body)
    except Exception as e:
        return None, "req-fail:%s" % e
    vd = d.get("videoDetails") or {}
    return bool(vd.get("isLive")), vd.get("title", "")


def oembed(vid):
    try:
        req = urllib.request.Request(
            "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=%s&format=json" % vid,
            headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


for q in sys.argv[1:]:
    print("=" * 70)
    print("QUERY:", q)
    cands = search_live(q)
    print("搜索命中 %d 条" % len(cands))
    for c in cands[:14]:
        live, t = check(c["id"])
        oe = oembed(c["id"])
        mark = "LIVE" if live else ("dead" if live is False else "??")
        print("  [%-4s] oembed=%s  %s  | %s | %s" % (mark, oe, c["id"], c["channel"][:22], (t or c["title"])[:62]))
