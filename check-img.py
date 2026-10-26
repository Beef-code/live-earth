# -*- coding: utf-8 -*-
"""逐个验证站内所有 type:img 直连图的可用性（含新增 20 个 NPS）。"""
import concurrent.futures as cf
import re
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")

s = open("index.html", encoding="utf-8").read()
i = s.index("const CAMS = [")
j = s.index("\n];", i)
arr = s[i:j]

# 抽出 name + src 配对（只取 type:"img" 且带固定 src 的）
rows = re.findall(
    r'\{name:"([^"]+)".*?place:"([^"]+)".*?type:"img", src:"([^"]+)"', arr)

targets = [(n, p, u) for n, p, u in rows if "{" not in u]
print("固定 URL 的直连图:", len(targets))


def chk(t):
    n, p, u = t
    req = urllib.request.Request(
        u, headers={"User-Agent": UA, "Referer": "https://beef-code.github.io/"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            d = r.read(4000)
            return n, u, r.status, len(d), r.headers.get("Content-Type", "")
    except Exception as e:
        return n, u, 0, 0, str(e)[:40]


bad = []
with cf.ThreadPoolExecutor(max_workers=14) as ex:
    for n, u, st, sz, ct in ex.map(chk, targets):
        if st != 200 or "image" not in ct:
            bad.append((n, u, st, ct))

print("失效:", len(bad))
for n, u, st, ct in bad:
    print("  ! %-22s %s  %s" % (n, st, u[-60:]))
