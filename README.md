# Live Earth

[简体中文](README.zh-CN.md) · **English**

A single-file globe of live cameras. Spin the planet, click a dot, watch what is happening there right now.

**Live site:** https://beef-code.github.io/live-earth/

---

## What it is

Everything lives in one `index.html`. No build step, no `npm install`, no backend.

- **3D globe** — MapLibre GL JS (via CDN), with camera pins drawn as a GL layer wrapped onto the sphere
- **137 cameras** — city skylines, harbours and fishing villages, volcanoes and glaciers, wildlife reserves, observatories, the International Space Station
- **Three source types, auto-detected** — YouTube embeds, direct HLS streams, and official snapshot images
- **Filters in the sidebar** — narrow by source (YouTube / HLS / snapshot / open API), by country, and by category; the pins on the globe are filtered along with the list
- **Bilingual, 中文 / English** — one toggle in the top-right corner, remembered across visits; every camera carries both languages
- **Local time on every pin** — ticking every second off the IANA timezone, so you never have to do the math

By category: cities 57 · coast & water 28 · nature 27 · wildlife 18 · night sky 4 · space 3

By source: YouTube 121 · snapshot 12 · HLS 3 · open API 1

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
| `cat` | ✅ | `城市` / `水乡` / `自然` / `野生动物` / `星空` / `太空` |
| `icon` | ✅ | A single emoji |
| `desc` | ✅ | One or two plain sentences about **what you actually see**. No "8K cinematic beauty" filler |
| `yt` | source | YouTube **video ID** (the 11 characters after `watch?v=`), not the full URL |
| `type` | source | `hls` / `img` / `sgapi`. Defaults to YouTube when omitted |
| `src` | source | `.m3u8` URL for `hls`; image URL for `img` |
| `refresh` | optional | Snapshot refresh interval in seconds, default 60 |
| `page` | optional | Original page, used by the "Open at source" button |
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

---

## Known limitations

- **Chinese platforms all block embedding.** Bilibili sends `X-Frame-Options: SAMEORIGIN`; CCTV's Yangshipin uses `CSP: frame-ancestors 'self'`; Douyin, Kuaishou, Huya and Douyu behave the same. Bilibili's API returns 403 with no CORS header when it sees a foreign `Origin`, so a static site cannot even fetch a stream URL. Domestic cameras therefore go through a **live keyframe snapshot** with an "Open at source" button to the actual room
- **SkylineWebcams and earthTV block embedding too** (`SAMEORIGIN`). Do not count on them to fill city slots
- **YouTube live IDs expire.** Restart a broadcast and the ID changes; cameras need re-verification periodically
- **No embeddable Kuala Lumpur skyline exists.** Everything searchable is a traffic camera or a clock; the KL pin uses `noembed` and links out
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
