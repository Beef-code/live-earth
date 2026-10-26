# 直播地球 · Live Earth

**简体中文** · [English](README.md)

一个单文件的「世界风景直播」地球仪。转地球 → 点一个点 → 就播那里的实况。

线上地址：https://beef-code.github.io/live-earth/

---

## 它是什么

`index.html` 一个文件装下全部东西，没有构建、没有依赖安装、没有后端：

- **3D 地球**：MapLibre GL JS（CDN 引入），机位点以 GL 图层贴在球面上
- **137 个机位**：城市天际线、港口渔村、火山冰川、野生动物保护区、天文台、国际空间站
- **点开就播**：YouTube 嵌入 / HLS 直连 / 官方快照三种源自动切换
- **每个点多带当地时间**：按 IANA 时区每秒刷新，不看表也知道那边几点

机位分布：城市 57 · 水乡 28 · 自然 27 · 野生动物 18 · 星空 4 · 太空 3

源类型分布：YouTube 121 · 官方快照 12 · HLS 直连 3 · 开放 API 1

---

## 加一个机位

所有机位都在 `index.html` 里的 `const CAMS = [...]` 数组中，加一行就多一个点。

### 字段

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `name` | ✅ | 唯一名称。地图点、列表、选中高亮都靠它，**不能重名** |
| `en` | ✅ | 英文名，显示在副标题 |
| `place` | ✅ | `国家 · 地区 · 更细`，例如 `尼泊尔 · 索卢昆布 · 海拔 3880 米` |
| `lat` / `lon` | ✅ | 十进制度。国际空间站填 `0, 0` 并加 `iss:true` |
| `tz` | ✅ | IANA 时区，例如 `Asia/Kuala_Lumpur`，用于当地时间 |
| `cat` | ✅ | `城市` / `水乡` / `自然` / `野生动物` / `星空` / `太空` |
| `icon` | ✅ | 单个 emoji |
| `desc` | ✅ | 一两句人话，写清画面里**能看到什么**，别写「8K 超清美景」这类空话 |
| `yt` | 源 | YouTube **视频 ID**（`watch?v=` 后面那 11 位，不是整条链接） |
| `type` | 源 | `hls` / `img` / `sgapi`，不填则按 `yt` 处理 |
| `src` | 源 | `hls` 填 `.m3u8` 地址；`img` 填快照图片地址 |
| `refresh` | 可选 | 快照刷新秒数，默认 60 |
| `page` | 可选 | 源站页面，用于「在源站打开」按钮 |
| `noembed` | 可选 | `true` = 该频道禁止第三方嵌入，不加载 iframe，改显示直达按钮 |
| `iss` | 可选 | `true` = 国际空间站，不落在地表、不参与地图选点 |

### 三个例子

YouTube 直播：

```js
{name:"富士山 · 河口湖", en:"Mount Fuji from Lake Kawaguchi", place:"日本 · 山梨 · 河口湖",
 lat:35.517, lon:138.753, yt:"bdUbACCWmoY", tz:"Asia/Tokyo", cat:"自然", icon:"🗻",
 desc:"从大石公园看富士山，逆富士就出自这一带。晴天率最高的富士山机位之一，清晨湖面最平。"}
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

---

## 已知限制

- **国内平台全部禁嵌**：B 站 `X-Frame-Options: SAMEORIGIN`、央视频 `CSP: frame-ancestors 'self'`，抖音/快手/虎牙/斗鱼同理；B 站 API 见外部 Origin 直接 403 且不带 CORS 头。所以国内机位只能走「实时关键帧快照」这条路，点「在源站打开」去 B 站看完整直播
- **SkylineWebcams / earthTV 也禁嵌**（`SAMEORIGIN`），别指望用它们补城市机位
- **YouTube 直播 ID 会失效**：主播重开一场直播就换 ID，需要定期重验
- **吉隆坡没有可嵌的天际线直播源**，全网搜到的都是监控头和时间钟，只能用 `noembed` 直达
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
