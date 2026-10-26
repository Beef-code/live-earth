# -*- coding: utf-8 -*-
"""只挑真正的实时机位：NPS 的 webcams-<park>/ 目录 + featurecontent/ard 大图。
排除地图、缩略图、示意图。"""
import concurrent.futures as cf
import re
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")

CODES = """acad bibe blca cany crla dena ever glac grca grsm hale isro joda katm
lavo maca mora olym redw romo yell yose zion kewe""".split()

PAT = re.compile(r'https://www\.nps\.gov/[^"\'\s>]+?\.(?:jpg|jpeg)', re.I)
BAD = re.compile(r'map|collage|_1\.jpg|100-?px|344-?px|med|thumbnail|logo|icon|'
                 r'web_1|terrain|locations', re.I)


def grab(code):
    url = "https://www.nps.gov/%s/learn/photosmultimedia/webcams.htm" % code
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", "ignore")
    except Exception:
        return code, []
    imgs = []
    for u in sorted(set(PAT.findall(html))):
        if BAD.search(u):
            continue
        # 只要 webcams- 目录 或 featurecontent 的 large 大图
        if "/webcams-" in u or ("/featurecontent/ard/webcams/images/" in u and "large" in u):
            imgs.append(u)
    return code, imgs


def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                              "Referer": "https://beef-code.github.io/"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return url, r.status, len(r.read())
    except Exception as e:
        return url, 0, 0


res = {}
with cf.ThreadPoolExecutor(max_workers=10) as ex:
    for code, imgs in ex.map(grab, CODES):
        if imgs:
            res[code] = imgs

urls = [u for v in res.values() for u in v]
print("候选:", len(urls))
good = []
with cf.ThreadPoolExecutor(max_workers=16) as ex:
    for u, st, sz in ex.map(check, urls):
        if st == 200 and sz > 40000:
            good.append((u, sz))
print("可用(>40KB):", len(good))
print()
for u, sz in sorted(good, key=lambda x: x[0]):
    park = u.split("/")[3] if "/webcams-" in u else "ARD"
    print("%-10s %5dKB  %s" % (park, sz // 1024, u.split("/")[-1] if "/webcams-" in u else u.split("/")[-1]))
