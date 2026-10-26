# Live Earth

[简体中文](README.zh-CN.md) · **English**

A single-file globe of live cameras. Spin the planet, click a dot, watch what is happening there right now.

**Live site:** https://beef-code.github.io/live-earth/

---

## What it is

Everything lives in one `index.html`. No build step, no `npm install`, no backend.

- **3D globe** — MapLibre GL JS (via CDN), with camera pins drawn as a GL layer wrapped onto the sphere
- **Country borders** — one thin white line over the imagery, toggleable from the top bar. **China uses the AMap / DataV standard boundary** (Taiwan, the South China Sea islands and the nine-dash line are all included); every other country comes from Natural Earth 110m. The two disputed segments Natural Earth draws inside Chinese territory — Aksai Chin and the McMahon line — are dropped entirely, so the China line is only ever the standard one
- **217 cameras** — city skylines, harbours and fishing villages, volcanoes and glaciers, wildlife reserves, observatories, the International Space Station — plus **69 recorded walking tours**, one per city
- **Five source types, auto-detected** — YouTube live embeds, YouTube walking-tour videos, Bilibili live-keyframe snapshots, direct HLS streams, and official snapshot images
- **Filters in the sidebar** — narrow by source (YouTube / Bilibili slow-live / HLS / snapshot / open API), by country, by category (city / coast / nature / wildlife / night sky / space / **walking tour**), and — for walking tours — by day or night and by **spring / summer / autumn / winter / tropics**; the pins on the globe are filtered along with the list
- **Bilingual, 中文 / English** — one toggle in the top-right corner, remembered across visits; every camera carries both languages
- **Local time on every pin** — ticking every second off the IANA timezone, so you never have to do the math

By category: cities 57 · coast & water 29 · nature 32 · wildlife 18 · night sky 8 · space 4 · **walking tours 69** (55 day / 14 night, 50 countries)

Walking tours by season: spring 7 · summer 18 · autumn 27 · winter 10 · tropics (no seasons) 7

By source: YouTube live 113 · YouTube walking tours 69 · Bilibili slow-live 24 · snapshot 7 · HLS 3 · open API 1

Every YouTube pin was re-verified as actually live on **2026-10-26**.

---

## Adding a camera

Every camera is one entry in the `const CAMS = [...]` array inside `index.html`. Add a line, get a pin.

### Fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | ✅ | Unique name. Drives the pin, the sidebar list, and selection highlighting — **must not repeat** |
| `en` | ✅ | English name, shown as the subtitle (and as the title when the UI is in English) |
| `place` | ✅ | `Country · Region · detail`, e.g. `Nepal · Solukhumbu · 3,880 m`. **The first segment is the country filter key** |
| `pEn` | ✅ | English `place`, same ` · ` structure. The first segment becomes the English country label |
| `dEn` | ✅ | English description, shown when the UI is in English |
| `lat` / `lon` | ✅ | Decimal degrees. For the ISS use `0, 0` plus `iss:true` |
| `tz` | ✅ | IANA timezone, e.g. `Asia/Kuala_Lumpur`, used for local time |
| `cat` | ✅ | `城市` / `水乡` / `自然` / `野生动物` / `星空` / `太空` / `漫游` (walking tour) |
| `walk` | optional | `true` = this is a **recorded** walking tour, not a live stream. Skips the liveness check and shows a "recorded" badge instead of LIVE |
| `tod` | with `walk` | `day` or `night`. Powers the extra ☀️/**🌙** filter and the tag next to the name |
| `season` | with `walk` | `spring` / `summer` / `autumn` / `winter` / `tropics`. Powers the 🍂 season filter; shows an icon after the name and as the tooltip |
| `len` | with `walk` | Runtime as it appears on YouTube, e.g. `1:12:40` |
| `icon` | ✅ | A single emoji |
| `desc` | ✅ | One or two plain sentences about **what you actually see**. No "8K cinematic beauty" filler |
| `yt` | source | YouTube **video ID** (the 11 characters after `watch?v=`), not the full URL |
| `type` | source | `hls` / `img` / `sgapi`. Defaults to YouTube when omitted |
| `src` | source | `.m3u8` URL for `hls`; image URL for `img` |
| `refresh` | optional | Snapshot refresh interval in seconds, default 60 |
| `page` | optional | Original page, used by the "Open at source" button |
| `bili` | optional | Bilibili room id. Marks the camera as Bilibili in the source filter and keeps its keyframe on a 30 s refresh |
| `noembed` | optional | `true` = channel blocks third-party embedding. Skips the iframe and shows a direct link instead |
| `iss` | optional | `true` = International Space Station. Not placed on the surface, excluded from map selection |

> `cat` values are Chinese because the UI is Chinese. Keep them as-is unless you translate the interface too.

### Examples

YouTube live stream:

```js
{name:"富士山 · 河口湖", en:"Mount Fuji from Lake Kawaguchi",
 pEn:"Japan · Yamanashi · Lake Kawaguchi", place:"日本 · 山梨 · 河口湖",
 lat:35.517, lon:138.753, yt:"bdUbACCWmoY", tz:"Asia/Tokyo", cat:"自然", icon:"🗻",
 desc:"从大石公园看富士山，逆富士就出自这一带。晴天率最高的富士山机位之一，清晨湖面最平。",
 dEn:"Mount Fuji from Oishi Park, home of the famous reflection. Clearest skies in the morning."}
```

Direct HLS stream (your own feed, or a broadcaster's):

```js
{name:"NASA 电视台", en:"NASA TV", place:"美国 · 佛罗里达 · 肯尼迪航天中心一带",
 lat:28.57, lon:-80.65, type:"hls",
 src:"https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8",
 page:"https://www.nasa.gov/live/", tz:"America/New_York", cat:"太空", icon:"📡",
 desc:"NASA 官方直播频道的直连流（Akamai），不经过 YouTube：火箭发射、空间站活动、任务直播都走这条。"}
```

Snapshot fallback (when no live stream exists, an `<img>` that reloads on a timer):

```js
{name:"维港夜景 · 慢直播", en:"Victoria Harbour Slow-Live", place:"中国 · 香港",
 lat:22.293, lon:114.169, type:"img",
 src:"https://i0.hdslb.com/bfs/live-key-frame/keyframe10260055000013131453n639q7.jpg",
 page:"https://live.bilibili.com/13131453", refresh:30, tz:"Asia/Hong_Kong", cat:"城市", icon:"🌃",
 desc:"B 站 24 小时慢直播间的实时关键帧快照，无人机视角看维多利亚港。"}
```

Embed-blocked channel (still listed, never loaded in an iframe):

```js
{name:"吉隆坡天际线", en:"KL Skyline", place:"马来西亚 · 吉隆坡",
 lat:3.157, lon:101.712, yt:"_1tcOO0CKsM", noembed:true,
 tz:"Asia/Kuala_Lumpur", cat:"城市", icon:"🇲🇾",
 desc:"吉隆坡市区天际线机位，双子塔在画面里。"}
```

All four examples above are real entries currently in the site.

---

## Language

The UI ships in Chinese and English. The toggle sits in the top-right corner, and the choice is remembered in `localStorage`.

- **Share a language directly:** `?lang=en` or `?lang=zh` on the URL overrides the stored preference, e.g. https://beef-code.github.io/live-earth/?lang=en
- **Adding a camera:** fill in `pEn` and `dEn` as well as `place` and `desc`, otherwise it falls back to Chinese in English mode
- **Category names** stay Chinese in the data (`城市`, `水乡`, …) because they are also the filter keys; `CAT_EN` maps them for display

## Walking tours are a different animal

Most of the site is live: fixed cameras and 24/7 streams. Walking tours are not. They are **recorded** first-person videos — someone walked through Lisbon for 78 minutes and uploaded it. 69 of them, one per city, 50 countries.

That difference matters in five places:

- **They never "die" the way live streams do.** A live ID expires the moment the broadcaster restarts; a recorded video keeps the same ID for years. So `check-live.py` treats them separately — `walk:true` goes through the oEmbed check only, and reports `VOD` instead of `LIVE`.
- **The badge says 🎬 步行漫游 · 录播**, not LIVE. Presenting a recording as a live feed would be a lie a viewer finds out in ten seconds anyway.
- **Day or night is measured, not guessed.** The `tod` field comes from looking at the actual thumbnail — 55 day walks, 14 night walks. There is no API that tells you "this walk is at night"; you have to see it. A luminance average alone is not enough (overcast London reads as dark as Vegas at night), so the borderline ones were inspected by eye.
- **Season is back-calculated from the upload date.** `season` takes each video's `publishDate` from the innertube `player` endpoint as a stand-in for the shooting month, then flips it for the southern hemisphere — December is summer in Auckland, Cape Town, Melbourne, Buenos Aires, Rio and Sydney. When the title names a season outright, the title wins: the Dubrovnik walk was uploaded in February but is titled "Perfect Summer Day". **The tropics do not get four seasons.** Inside ±15° latitude there is no seasonal cycle, so those seven walks (Bali, Bangkok, Ho Chi Minh City, Kuala Lumpur, Manila, Singapore, Lima) are tagged `tropics` rather than forced into "summer". The per-video evidence — ID, original title, publish date, final season — is in `walk-seasons.json` if you want to check any single entry.
- **The map pin is the city centre**, not the exact street. A 90-minute walk covers a whole district; a single point would be false precision.

If a walking tour ever disappears, the replacement path is different too: search YouTube for `<city> walking tour 4k`, keep candidates whose title contains the city name and whose duration is 15+ minutes, and require oEmbed `200`.

---

## Two pitfalls worth knowing

### 1. Error 153 — "Video player configuration error"

The debug payload behind it reads `embedder.identity.missing.referrer`: **the YouTube player is not receiving an HTTP Referer**.

- The iframe already carries `referrerpolicy="strict-origin-when-cross-origin"`, and the `<head>` has a matching `<meta name="referrer">`. Served over https, it just works
- **Opening the html by double-clicking (`file://`) will always throw 153** — a `file://` page has no origin to send. This is not a broken site
- For local work, serve it over http (see below)

### 2. Embedding disabled by the channel

Channel owners can switch off "Allow embedding". No amount of markup will play those; that is what `noembed:true` is for.

**How to check** (`200` = embeddable, `401` = blocked):

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json"
```

**Confirm it is actually live right now** (otherwise you are linking a finished broadcast):

```bash
curl -s "https://www.youtube.com/watch?v=VIDEO_ID" -H "User-Agent: Mozilla/5.0" \
  | grep -c '"isLive":true'
```

Hard-won lesson: **embedding permission is per channel, and sibling channels differ.** The whole `WEBCAM NEPAL LIVE` channel is embed-blocked, while `WEBCAM NEPAL NATURE` and `WEBCAM NEPAL HIMALAYA` are fine. Check the channel first instead of testing camera by camera.

---

## Local preview

```bash
cd <project directory>
python -m http.server 8770
```

Then open http://127.0.0.1:8770/

Do **not** open `index.html` directly from disk — that is pitfall 1, and you will see Error 153 on every camera.

---

## Deploying

GitHub Pages, `main` branch, repo root. Pure static.

1. Open https://github.com/Beef-code/live-earth
2. **Add file** → **Upload files**, then drag in `index.html` (drag the file, not the folder — a folder creates a subdirectory and Pages will not find the homepage)
3. **Commit changes**, wait 30–60 seconds
4. Hard-refresh the live URL with `Ctrl + Shift + R`

Or from the command line:

```bash
git clone https://github.com/Beef-code/live-earth.git
cd live-earth
# replace index.html
git commit -am "Update cams" && git push
```

---

## Validation

Run the checker before you push. It catches duplicate IDs, duplicate names, missing fields, out-of-range coordinates, and cameras with no source:

```bash
node validate.js index.html
```

Only trust it when it prints `ALL CHECKS PASSED`.

That checker is **offline** — it cannot tell you whether a stream is still running. Run this one too before publishing, or periodically:

```bash
python check-live.py index.html
```

It goes out to the network and verifies every pin: YouTube via `videoDetails.isLive`, Bilibili via `live_status` plus a keyframe fetch, everything else via a HEAD on the source URL. Exit code is `0` when every camera is alive, `1` when something needs replacing. It takes about ten seconds.

---

## Known limitations

- **Chinese platforms all block embedding.** Bilibili's `/blanc/{room}` player looked like the exception — it sends **no `X-Frame-Options` and no CSP**, and the stream API answers 200 when no Referer is sent — but the player stays black in practice (verified in headless Edge and in a real browser), so the Bilibili play-through was **removed**. What actually works is the keyframe: Bilibili's CDN answers **403 to a foreign Referer and 200 to no Referer at all**, so the `<img id="snap">` must carry `referrerpolicy="no-referrer"` — that one attribute is the whole trick. Everything else about Chinese platforms still holds: Bilibili sends `X-Frame-Options: SAMEORIGIN`; CCTV's Yangshipin uses `CSP: frame-ancestors 'self'`; Douyin, Kuaishou, Huya and Douyu behave the same. Bilibili's API returns 403 with no CORS header when it sees a foreign `Origin`, so a static site cannot even fetch a stream URL. Domestic cameras therefore go through a **live keyframe snapshot** with an "Open at source" button to the actual room
- **SkylineWebcams and earthTV block embedding too** (`SAMEORIGIN`). Do not count on them to fill city slots
- **YouTube live IDs expire.** A broadcaster restarting the stream gets a brand-new 11-character ID; the old one immediately becomes "This live stream recording is not available" and the pin shows a dead iframe. This is not rare — a full sweep on 2026-10-26 found **30 of 121 YouTube pins dead**. Re-verify periodically.
  - Reliable check: `POST https://www.youtube.com/youtubei/v1/player?prettyPrint=false` with `{"context":{"client":{"clientName":"WEB","clientVersion":"2.20241010.01.00"}},"videoId":"<ID>"}` and read `videoDetails.isLive`. `playabilityStatus` is `UNPLAYABLE` even for healthy streams (no signature deciphering), so ignore it.
  - Do **not** scrape the watch page: after a few dozen requests YouTube serves a 3 KB reCAPTCHA page instead of the video, which silently reads as "dead" and produced 30 false negatives before this was caught.
  - Do **not** use `maxresdefault_live.jpg` as a liveness probe: it returns `200` for ended streams too.
  - Finding the replacement: `https://www.youtube.com/channel/<channelId>/live` 302s to whatever that channel is streaming **right now**. For single-camera channels that is exactly right, but multi-camera channels (EarthCam, GiGAeyes Live TV) will happily hand you a different city — so match location words in the returned title before accepting it.
- **Some channels block embedding outright** — `oEmbed` answers **401** instead of 200, and there is no way around it. The KL skyline and Lukla airport pins are in that bucket, so they carry `noembed:true` and skip the iframe entirely.
- **YouTube `_live` thumbnails are the workaround for blocked channels.** `https://i.ytimg.com/vi/<ID>/maxresdefault_live.jpg` is the current live frame, it has **no hotlink protection at all** (works with any Referer, even `file://`), and it falls back through `hqdefault_live` → `hqdefault`. The catch is freshness: `Cache-Control: max-age=300`, so the CDN serves the same frame for **5 minutes** and a cache-busting query string does not help. Good enough as a still, useless as video. Those two pins use exactly this: a live still plus a button out
- Stateless and backend-free: no favourites, no proxying

---

## Stack

| Component | Version | Role |
| --- | --- | --- |
| MapLibre GL JS | 5.24.0 | 3D globe and camera layer |
| hls.js | 1.5.18 | `.m3u8` playback (Safari uses native HLS) |

Both loaded from jsDelivr. No bundler.

---

## Credits

All footage belongs to the respective broadcasters and channels. This project only **aggregates and links out to publicly available live streams** — nothing is recorded, proxied, or redistributed. If a channel owner would rather not be listed, delete that one line from `CAMS`.
