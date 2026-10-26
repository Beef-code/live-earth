# 直播地球 · Live Earth

**简体中文** · [English](README.md)

一个单文件的「世界风景直播」地球仪。转地球 → 点一个点 → 就播那里的实况。

线上地址：https://beef-code.github.io/live-earth/

---

## 它是什么

`index.html` 一个文件装下全部东西，没有构建、没有依赖安装、没有后端：

- **3D 地球**：MapLibre GL JS（CDN 引入），机位点以 GL 图层贴在球面上
- **国界**：影像上压一层细白线，右上角「🗺 边界」可开关。**中国用高德（DataV／AMap 坐标系）标准国界**，含台湾、南海诸岛和九段线；其余国家用 Natural Earth 110m。NE 在中国境内画的那两段争议线（阿克赛钦、藏南麦克马洪线）整段剔除，中国一侧只认高德那条线
- **243 个机位，两种看法**：174 个定点直播——城市天际线、港口渔村、火山冰川、野生动物保护区、天文台、国际空间站、南极科考站、巴拿马运河，以及 **27 个美国国家公园官方直连机位**；再加 **69 条步行漫游录播**，每城一条
- **点开就播**：YouTube 直播嵌入 / YouTube 步行漫游录播 / B 站实时关键帧 / HLS 直连 / 官方快照五种源自动切换
- **左栏是两层的**：最上面先选**观赏类型**——📡 **定点直播**（148 个固定机位，看的是此时此刻）或 🚶 **步行漫游**（69 条录播，有人替你在那条街上走了一遍）。这两个是并列的两种观看方式，不是题材。定点直播之下再按来源（YouTube / B 站慢直播 / 直连流 / 快照 / 开放 API）和题材（城市 / 水乡 / 自然 / 野生动物 / 星空 / 太空）筛；**白天 / 夜晚**和**春 / 夏 / 秋 / 冬 / 热带**是步行漫游独有的两个维度，选定点直播时整块不出现。切换类型会自动清掉上一层不再适用的筛选，各下拉的计数都以当前类型为分母，不会出现「写着 5 条、点进去 0 条」。地图上的点跟着一起过滤
- **中英双语**：右上角一键切换，选择记在 localStorage；每个机位都带两套文案
- **每个点多带当地时间**：按 IANA 时区每秒刷新，不看表也知道那边几点

机位分布：城市 57 · 水乡 33 · 自然 51 · 野生动物 22 · 星空 8 · 太空 3 · **步行漫游 69**（白天 55 / 夜晚 14）。全部机位覆盖 **73 个国家与地区**，包括南极洲

漫游季节分布：春 7 · 夏 18 · 秋 27 · 冬 10 · 热带（无四季）7

源类型分布：YouTube 直播 113 · YouTube 步行漫游 69 · B 站慢直播 24 · 官方快照 7 · HLS 直连 3 · 开放 API 1

所有 YouTube 机位已于 **2026-10-26** 全量复核为「确实在播」。

---

## 加一个机位

所有机位都在 `index.html` 里的 `const CAMS = [...]` 数组中，加一行就多一个点。

### 字段

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `name` | ✅ | 唯一名称。地图点、列表、选中高亮都靠它，**不能重名** |
| `en` | ✅ | 英文名，英文界面下作为标题 |
| `place` | ✅ | `国家 · 地区 · 更细`，例如 `尼泊尔 · 索卢昆布 · 海拔 3880 米`。**第一段就是国家筛选的键** |
| `pEn` | ✅ | 英文 `place`，同样用 ` · ` 分段；第一段决定英文界面里的国家名 |
| `dEn` | ✅ | 英文描述，英文界面下显示 |
| `lat` / `lon` | ✅ | 十进制度。国际空间站填 `0, 0` 并加 `iss:true` |
| `tz` | ✅ | IANA 时区，例如 `Asia/Kuala_Lumpur`，用于当地时间 |
| `cat` | ✅ | `城市` / `水乡` / `自然` / `野生动物` / `星空` / `太空` / `漫游`（步行漫游） |
| `walk` | 可选 | `true` = 这条是**录播**的步行漫游，不是直播。会跳过判活检查，角标显示「录播」而不是 LIVE |
| `tod` | 配合 `walk` | `day` 或 `night`，驱动额外的 ☀️/**🌙** 筛选和名字后面的标记 |
| `season` | 配合 `walk` | `spring` / `summer` / `autumn` / `winter` / `tropics`，驱动 🍂 季节筛选，卡片名字后面挂对应图标并作为 tooltip |
| `len` | 配合 `walk` | YouTube 上显示的时长，如 `1:12:40` |
| `icon` | ✅ | 单个 emoji |
| `desc` | ✅ | 一两句人话，写清画面里**能看到什么**，别写「8K 超清美景」这类空话 |
| `yt` | 源 | YouTube **视频 ID**（`watch?v=` 后面那 11 位，不是整条链接） |
| `type` | 源 | `hls` / `img` / `sgapi`，不填则按 `yt` 处理 |
| `src` | 源 | `hls` 填 `.m3u8` 地址；`img` 填快照图片地址 |
| `refresh` | 可选 | 快照刷新秒数，默认 60 |
| `srcTpl` | `img` 专用 | 地址里**带时间戳**的站点写模板代替 `src`。例如澳洲南极局 `.../{Y}/{M}/{D}/D{DD}{MM}{YY}{HH}{NN}s.jpg`，取图时按当前 UTC 替换：`{Y}` 四位年、`{YY}` 两位年、`{M}`/`{MM}` 月、`{D}`/`{DD}` 日、`{HH}` 时、`{NN}` 分 |
| `tplStep` | 配合 `srcTpl` | 该站出图的**分钟间隔**。各站不一样（Davis/Mawson 每 5 分钟、Casey 每 3 分钟），按它对齐到最近一格；这一格还没生成时自动再往前退一格，最多退 5 格 |
| `page` | 可选 | 源站页面，用于「在源站打开」按钮 |
| `bili` | 可选 | B 站房间号。用于来源筛选归入「B 站慢直播」，并让关键帧按 30 秒刷新 |
| `noembed` | 可选 | `true` = 该频道禁止第三方嵌入，不加载 iframe，改显示直达按钮 |
| `iss` | 可选 | `true` = 国际空间站，不落在地表、不参与地图选点 |

### 三个例子

YouTube 直播：

```js
{name:"富士山 · 河口湖", en:"Mount Fuji from Lake Kawaguchi",
 pEn:"Japan · Yamanashi · Lake Kawaguchi", place:"日本 · 山梨 · 河口湖",
 lat:35.517, lon:138.753, yt:"bdUbACCWmoY", tz:"Asia/Tokyo", cat:"自然", icon:"🗻",
 desc:"从大石公园看富士山，逆富士就出自这一带。晴天率最高的富士山机位之一，清晨湖面最平。",
 dEn:"Mount Fuji from Oishi Park, home of the famous reflection. Clearest skies in the morning."}
```

HLS 直连（自有流、电视源，不经过 YouTube）：

```js
{name:"NASA 电视台", en:"NASA TV", place:"美国 · 佛罗里达 · 肯尼迪航天中心一带",
 lat:28.57, lon:-80.65, type:"hls",
 src:"https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8",
 page:"https://www.nasa.gov/live/", tz:"America/New_York", cat:"太空", icon:"📡",
 desc:"NASA 官方直播频道的直连流（Akamai），不经过 YouTube：火箭发射、空间站活动、任务直播都走这条。"}
```

官方快照（拿不到直播流时的兜底，`<img>` 定时换图）：

```js
{name:"维港夜景 · 慢直播", en:"Victoria Harbour Slow-Live", place:"中国 · 香港",
 lat:22.293, lon:114.169, type:"img",
 src:"https://i0.hdslb.com/bfs/live-key-frame/keyframe10260055000013131453n639q7.jpg",
 page:"https://live.bilibili.com/13131453", refresh:30, tz:"Asia/Hong_Kong", cat:"城市", icon:"🌃",
 desc:"B 站 24 小时慢直播间的实时关键帧快照，无人机视角看维多利亚港。"}
```

禁嵌频道（照常收录，但不加载 iframe）：

```js
{name:"吉隆坡天际线", en:"KL Skyline", place:"马来西亚 · 吉隆坡",
 lat:3.157, lon:101.712, yt:"_1tcOO0CKsM", noembed:true,
 tz:"Asia/Kuala_Lumpur", cat:"城市", icon:"🇲🇾",
 desc:"吉隆坡市区天际线机位，双子塔在画面里。"}
```

---

## 语言 / 双语

界面有中文和英文两套，右上角一键切换，选择存进 `localStorage`。

- **直接分享某一种语言**：URL 上加 `?lang=en` 或 `?lang=zh` 会覆盖已存偏好，例如 https://beef-code.github.io/live-earth/?lang=en
- **加机位时**：`pEn` 和 `dEn` 要跟 `place`、`desc` 一起填，否则英文界面会退回中文
- **类型名**（`城市`/`水乡`…）在数据里保持中文，因为它同时是筛选的键；英文显示靠 `CAT_EN` 映射

## 步行漫游是另一类东西

站里绝大多数是直播：固定机位和 24 小时流。步行漫游不是——它是**录播**的第一视角走路视频，有人替你在里斯本走了 78 分钟然后传上来。一共 69 条，每个城市一条，覆盖 50 个国家。

这个差别体现在五处：

- **它们不会像直播那样「死掉」。** 直播一重启 ID 就作废；录播视频的 ID 几年都不变。所以 `check-live.py` 单独处理：`walk:true` 只走 oEmbed 检查，报 `VOD` 而不是 `LIVE`。
- **角标写的是 🎬 步行漫游 · 录播**，不是 LIVE。把录播标成直播，观众十秒钟就能看穿。
- **白天/夜晚是看出来的，不是猜的。** `tod` 字段来自逐条看封面：55 条白天、14 条夜晚。没有任何接口会告诉你「这条是夜走」，只能看。光算平均亮度也不够——阴天的伦敦和夜里的拉斯维加斯亮度差不多——所以边界样本都是肉眼过的。
- **四季是从发布时间倒推的。** `season` 取每条视频的 `publishDate`（innertube `player` 接口），当拍摄月份用，再按南北半球换算——奥克兰、开普敦、墨尔本、布宜诺斯艾利斯、里约、悉尼这些南半球城市，12 月是夏天。标题里明写了季节的以标题为准，比如杜布罗夫尼克那条 2 月发布却写着「Perfect Summer Day」。**热带不套四季**：南北纬 15° 以内常年没有季节交替，单列 `tropics`（巴厘、曼谷、胡志明、吉隆坡、马尼拉、新加坡、利马，7 条），硬标成「夏」是错的。逐条依据（视频 ID、原标题、发布时间、最终季节）存在 `walk-seasons.json`，要复查哪一条直接查这张表。
- **地图上的点是城市中心**，不是精确街道。90 分钟的走路覆盖一整个区，标一个点反而是假的精确。

万一某条漫游失效了，补的办法也不一样：搜 `<城市名> walking tour 4k`，标题里必须含城市名、时长 15 分钟以上，再验 oEmbed 是否 `200`。

---

## 两个必须知道的坑

### 坑一：Error 153 · Video player configuration error

错误码含义是 `embedder.identity.missing.referrer`——**YouTube 内嵌播放器收不到 HTTP Referer**。

- 页面里已经写了 `referrerpolicy="strict-origin-when-cross-origin"`（iframe 上）和 `<meta name="referrer">`（head 里），线上 https 页面正常
- **直接双击 html 文件（`file://`）打开必然报 153**，因为 file:// 没有 origin 可发。这不是站点坏了
- 本地调试请起 http 服务，见下方「本地预览」

### 坑二：频道关闭了第三方嵌入

频道主可以在后台关掉「允许嵌入」，这种视频怎么调都播不出来，`noembed:true` 让它显示直达按钮而不是报错。

**判别方法**（`200` = 可嵌，`401` = 禁嵌）：

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json"
```

**顺手确认它现在真的在直播**（否则点开是个已结束的录像）：

```bash
curl -s "https://www.youtube.com/watch?v=VIDEO_ID" -H "User-Agent: Mozilla/5.0" \
  | grep -c '"isLive":true'
```

跑出一条经验：同一个运营方的多个频道权限可能不同。例如 **WEBCAM NEPAL LIVE 整频道禁嵌**，而 **WEBCAM NEPAL NATURE / HIMALAYA 可嵌**——选题先查频道，别一条条试。

---

## 本地预览

```bash
cd <本项目目录>
python -m http.server 8770
```

然后打开 http://127.0.0.1:8770/

**不要**直接双击 `index.html`——会踩坑一的 Error 153。

---

## 部署

GitHub Pages，`main` 分支根目录，纯静态：

1. 打开 https://github.com/Beef-code/live-earth
2. **Add file** → **Upload files** → 拖入 `index.html`（拖文件，不要拖文件夹，否则会变成子目录）
3. **Commit changes**，等 30–60 秒
4. `Ctrl + Shift + R` 硬刷新线上地址

或者命令行：

```bash
git clone https://github.com/Beef-code/live-earth.git
cd live-earth
# 替换 index.html
git commit -am "Update cams" && git push
```

---

## 数据校验

改完机位别直接推，先跑一遍检查（重复 ID、重复名称、缺字段、坐标越界、无源机位）：

```bash
node validate.js index.html
```

输出 `ALL CHECKS PASSED` 才算过。

但它是**离线的**，判断不了直播是否还在播。发布前（或定期）再跑这个：

```bash
python check-live.py index.html
```

它会联网逐个复核：YouTube 读 `videoDetails.isLive`，B 站读 `live_status` 并取一次关键帧，其他源直接 HEAD。全部在播退出码为 `0`，有失效机位为 `1`。跑一遍十秒左右。

---

## 已知限制

- **国内平台基本都禁嵌。B 站 `/blanc/{room}` 播放器看着像例外**——它确实没有 `X-Frame-Options` 也没有 CSP，取流 API 不带 Referer 也返回 200——但实测播放器一直是黑屏（无头 Edge 和真实浏览器都试过），所以 B 站试播按钮已经**移除**。真正能用的只有关键帧：B 站 CDN 对「外部 Referer」一律 403、对「完全不带 Referer」返回 200，所以 `<img id="snap">` 必须带 `referrerpolicy="no-referrer"`，就差这一个属性。其余限制照旧：央视频 `CSP: frame-ancestors 'self'`，抖音/快手/虎牙/斗鱼同样禁嵌，B 站 API 见外部 Origin 直接 403 且无 CORS 头
- **SkylineWebcams / earthTV 也禁嵌**（`SAMEORIGIN`），别指望用它们补城市机位
- **能写死的 HLS 直连视频极少，而且会「假活」**。判断一条 m3u8 不能只看 master 是不是 200——必须顺着链子拉到 `.ts` 分片，再看子清单里有没有 `EXT-X-MEDIA-SEQUENCE` 在滚动。2026-10-26 踩过的两个例子：
  - **NASA TV**（`ntv1.akamaized.net/hls/live/2014075/...`）：master 返回 200、`Access-Control-Allow-Origin: *` 齐全，看着完全正常——但 `Last-Modified` 停在 **2024 年 3 月**，里面的 `master_500.m3u8` 是 **404**。整个是条化石流，已删除
  - **基韦斯特海滩**（`streamlock.net:444`）：域名能解析，但 444 / 1935 两个端口全部连不上（curl 返回 000），服务方早已停播，已删除
  - 唯一还在滚动的只剩 **佛罗里达 30A 海岸**（`30a-tv.com/beachy.m3u8`），master、子清单、分片三级全 200 且带 CORS。但注意它的分片路径是 `2019_11_06_...`，属于**循环播放的录像**，不是真·实时镜头
- **美国国家公园管理局（NPS）是最大的非 YouTube 来源**：`https://www.nps.gov/webcams-<公园代码>/<名字>.jpg` 是官方直连图，无防盗链、无广告、无 YouTube，分辨率普遍 1080p 至 4K（皇家岛那张是 3840×2160）。各公园的机位清单在其 `/learn/photosmultimedia/webcams.htm` 页面里，按公园代码逐个抓即可
- **YouTube 直播 ID 会失效**：主播重开直播就换一个新的 11 位 ID，旧 ID 立刻变成「This live stream recording is not available」，机位点开就是死 iframe。这不是偶发——2026-10-26 全量扫了一遍，**121 个 YouTube 机位里 30 个已经结束**。需要定期重验。
  - 可靠判活：`POST https://www.youtube.com/youtubei/v1/player?prettyPrint=false`，body 为 `{"context":{"client":{"clientName":"WEB","clientVersion":"2.20241010.01.00"}},"videoId":"<ID>"}`，读 `videoDetails.isLive`。注意 `playabilityStatus` 即使是正常直播也返回 `UNPLAYABLE`（不做签名解密），别拿它判断。
  - **不要**去爬 watch 页面：请求几十次后 YouTube 会返回一个 3KB 的 reCAPTCHA 页面而不是视频页，看起来就像「视频已死」，这次就是这样误判出 30 个假死。
  - **不要**用 `maxresdefault_live.jpg` 判活：已结束的直播它照样返回 200。
  - 找替代：`https://www.youtube.com/channel/<channelId>/live` 会 302 跳到该频道**此刻**在播的那一场。单机位频道正好对，但 EarthCam、GiGAeyes Live TV 这类多机位频道会直接给你另一个城市——所以必须用标题里的地点词校验，否则纽约时代广场会被换成都柏林。
- **部分频道直接关闭嵌入**：`oEmbed` 返回 **401** 而不是 200，没有绕过的办法。吉隆坡天际线、卢卡拉机场这两个机位就属于这类，所以带 `noembed:true`，根本不加载 iframe。
- **YouTube 的 `_live` 缩略图是这类频道的解法**：`https://i.ytimg.com/vi/<ID>/maxresdefault_live.jpg` 就是当前直播帧，**完全没有防盗链**（任意 Referer 都能取，`file://` 也行），并会按 `hqdefault_live` → `hqdefault` 逐级回退。代价是新鲜度：`Cache-Control: max-age=300`，CDN 同一帧会持续返回 **5 分钟**，加随机参数也绕不过去。当静帧够用，当视频不行。这两个机位就是这么处理的：实时封面 + 一个跳转按钮
- 纯静态、无后端：不能保存收藏，也不能代理播放

---

## 技术栈

| 组件 | 版本 | 用途 |
| --- | --- | --- |
| MapLibre GL JS | 5.24.0 | 3D 地球与机位图层 |
| hls.js | 1.5.18 | `.m3u8` 直连播放（Safari 走原生） |

均通过 jsDelivr CDN 引入，无打包步骤。

---

## 声明

所有直播画面的版权归各源站与频道方所有。本项目只做**公开直播的聚合与跳转播放**，不转存、不代理、不二次分发。若某频道主不希望被收录，删掉对应那一行即可。
