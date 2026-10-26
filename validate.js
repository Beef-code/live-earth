const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const start = html.indexOf("const CAMS = [");
const end = html.indexOf("];", start);
if (start < 0 || end < 0) { console.error("CAMS array not found"); process.exit(1); }
const arrText = html.slice(start + "const CAMS = ".length, end + 1);
let CAMS;
try { CAMS = eval(arrText); } catch (e) { console.error("EVAL FAIL:", e.message); process.exit(1); }
console.log("total cams:", CAMS.length);
// checks
const ytIds = {}, names = {};
const SEASONS = ["spring", "summer", "autumn", "winter", "tropics"];
let problems = 0;
for (const c of CAMS) {
  if (c.yt && ytIds[c.yt]) { console.error("DUP yt id:", c.yt, c.name, "vs", ytIds[c.yt]); problems++; }
  if (c.yt) ytIds[c.yt] = c.name;
  if (names[c.name]) { console.error("DUP name:", c.name); problems++; }
  names[c.name] = true;
  if (!c.name || !c.place || !c.desc || !c.icon || !c.cat || !c.tz) { console.error("MISSING field:", c.name); problems++; }
  if (typeof c.lat !== "number" || typeof c.lon !== "number") { console.error("BAD lat/lon:", c.name); problems++; }
  if (!c.iss && (Math.abs(c.lat) > 90 || Math.abs(c.lon) > 180)) { console.error("OUT OF RANGE:", c.name); problems++; }
  if (!c.yt && !c.channel && !c.src && !c.type) { console.error("NO SOURCE:", c.name); problems++; }
  // 漫游必须有季节；非漫游不应带季节字段（季节只对录播漫游有意义）
  if (c.walk) {
    if (c.tod !== "day" && c.tod !== "night") { console.error("BAD tod:", c.name, c.tod); problems++; }
    if (SEASONS.indexOf(c.season) < 0) { console.error("BAD/MISSING season:", c.name, c.season); problems++; }
    if (Math.abs(c.lat) < 15 && c.season !== "tropics") { console.error("HOT BELT should be tropics:", c.name, c.season, c.lat); problems++; }
    if (Math.abs(c.lat) >= 23.5 && c.season === "tropics") { console.error("TEMPERATE marked tropics:", c.name, c.lat); problems++; }
  } else if (c.season) {
    console.error("SEASON on non-walk cam:", c.name); problems++;
  }
  if (c.srcTpl) {
    if (c.type !== "img") { console.error("srcTpl without type:img:", c.name); problems++; }
    if (c.src) { console.error("srcTpl and src both set:", c.name); problems++; }
    if (!/\{NN\}/.test(c.srcTpl)) { console.error("srcTpl missing {NN}:", c.name); problems++; }
    if (typeof c.tplStep !== "number" || c.tplStep < 1) { console.error("srcTpl missing tplStep:", c.name); problems++; }
    if (c.refresh && c.refresh !== c.tplStep * 60) { console.error("refresh != tplStep*60:", c.name, c.refresh, c.tplStep); problems++; }
  } else if (c.tplStep) {
    console.error("tplStep without srcTpl:", c.name); problems++;
  }
  if (c.type === "frame" || c.frame) {
    console.error("frame-embed cam (EarthCam) is not supported — see notes:", c.name); problems++;
  }
}
// cat coverage
const byCat = {};
CAMS.forEach(c => byCat[c.cat] = (byCat[c.cat]||0)+1);
console.log("by category:", JSON.stringify(byCat));
const ytCount = CAMS.filter(c=>c.yt||c.channel).length;
console.log("youtube cams:", ytCount);
// overall html sanity: balanced tags quick check on script block
if (html.includes("const CAMS = [") && html.trim().endsWith("</html>")) console.log("html structure OK");
console.log(problems === 0 ? "ALL CHECKS PASSED" : `PROBLEMS: ${problems}`);
process.exit(problems === 0 ? 0 : 2);
