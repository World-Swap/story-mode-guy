#!/usr/bin/env python3
"""Free interactive tools/calculators -> /tools/*.html + /tools/index.html.
Link-magnet pages that rank for tool searches and funnel to the matching guide.
All self-contained static HTML + inline JS (no APIs). Injects /tools/ into sitemap.
Run from repo root: python3 promo/build/tools.py
"""
import pathlib, json, html
ROOT = pathlib.Path("/home/user/story-mode-guy")
OUT = ROOT / "tools"; OUT.mkdir(exist_ok=True)

CSS = """
:root{--parch:#fefffc;--ink:#1b1b20;--char:#3a3a40;--ash:#6a6a72;--fog:#b4b8b4;--mist:#e3e6ea;
--blue:#41a1cf;--serif:'Fraunces',Georgia,serif;--sans:'Inter',system-ui,sans-serif;--accent:__ACCENT__}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);color:var(--char);background:var(--parch);line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.nav{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:14px;justify-content:center;background:rgba(255,255,255,.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--mist);padding:12px 16px}
.nav .brand{display:flex;align-items:center;gap:9px;font-family:var(--serif);font-size:17px;color:var(--ink)}
.nav .brand img{width:30px;height:30px;border-radius:50%}
.nav .sp{flex:1}.nav .lnk{font-size:14px;font-weight:500;color:var(--char)}
.wrap{max-width:680px;margin:0 auto;padding:40px 22px 30px}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:10px}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(28px,4.6vw,40px);line-height:1.1;letter-spacing:-.02em;color:var(--ink);margin-bottom:10px}
.sub{font-size:18px;color:var(--ash);margin-bottom:26px}
.tool{background:#fff;border:1px solid var(--mist);border-radius:16px;padding:24px 22px;box-shadow:0 10px 34px rgba(0,0,0,.05)}
label{display:block;font-size:13px;font-weight:600;color:var(--ash);text-transform:uppercase;letter-spacing:.05em;margin:14px 0 6px}
input,select{width:100%;font-family:var(--sans);font-size:17px;padding:11px 12px;border:1px solid var(--mist);border-radius:10px;background:var(--parch);color:var(--ink)}
input:focus,select:focus{outline:2px solid var(--accent);border-color:transparent}
.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.out{margin-top:22px;background:var(--parch);border:1px dashed var(--mist);border-radius:12px;padding:18px 18px}
.out .big{font-family:var(--serif);font-size:30px;color:var(--ink);font-weight:600}
.out .lab{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--ash);margin-bottom:2px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.pill{display:inline-block;background:var(--accent);color:#fff;font-size:12px;font-weight:600;padding:3px 10px;border-radius:20px}
.note{font-size:13px;color:var(--ash);margin-top:12px}
.cta{background:linear-gradient(135deg,var(--accent),#0b1220);color:#fff;border-radius:16px;padding:22px 22px;margin-top:30px;text-align:center}
.cta h3{color:#fff;font-family:var(--serif);font-weight:600;font-size:21px;margin-bottom:6px}
.cta p{color:rgba(255,255,255,.9);margin-bottom:14px;font-size:15px}
.cta a.btn{display:inline-block;background:#fff;color:#111;font-weight:600;padding:11px 22px;border-radius:44px}
.cta a.btn:hover{text-decoration:none;filter:brightness(.97)}
.foot{border-top:1px solid var(--mist);margin-top:30px;padding:24px 22px;text-align:center;font-size:13px;color:var(--fog);max-width:680px;margin:30px auto 0}
.foot a{color:var(--ash)}
ul.check{list-style:none;padding:0;margin:6px 0}
ul.check li{padding:9px 0;border-bottom:1px solid var(--mist);display:flex;align-items:center;gap:10px;font-size:16px;color:var(--ink)}
ul.check input{width:20px;height:20px;flex:0 0 auto}
ul.check li.done{color:var(--fog);text-decoration:line-through}
.btnrow{display:flex;gap:10px;margin-top:14px}
button.act{font-family:var(--sans);font-size:14px;font-weight:600;padding:9px 16px;border-radius:22px;border:1px solid var(--mist);background:#fff;color:var(--char);cursor:pointer}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-top:12px}
.tcard{display:block;border:1px solid var(--mist);border-radius:14px;padding:18px;background:#fff;transition:transform .15s}
.tcard:hover{transform:translateY(-2px);text-decoration:none}
.tcard h3{font-family:var(--serif);font-size:19px;color:var(--ink);margin:0 0 4px}
.tcard p{font-size:14px;color:var(--ash);margin:0}
"""

def nav(): return ('<div class="nav"><a class="brand" href="/"><img src="/smg-logo.png" alt="Story Mode Guy">Story Mode Guy</a>'
    '<span class="sp"></span><a class="lnk" href="/tools/">Tools</a><a class="lnk" href="/learn/">Learn</a><a class="lnk" href="/blog/">Journal</a></div>')
FOOT = ('<div class="foot">© 2026 Story Mode Guy · <a href="/">storymodeguy.com</a> · '
        '<a href="/tools/">Free tools</a> · <a href="/learn/">Guides</a> · <a href="/blog/">Journal</a></div>')

def shell(t):
    body = t["body"]
    cta = (f'<div class="cta"><h3>{html.escape(t["cta_h"])}</h3><p>{html.escape(t["cta_p"])}</p>'
           f'<a class="btn" href="{t["cta_url"]}">{html.escape(t["cta_btn"])} →</a></div>')
    # FAQ block + FAQPage schema
    faq_html = ""; schemas = [{
        "@context":"https://schema.org","@type":"SoftwareApplication","name":t["title"],
        "applicationCategory":"MultimediaApplication","operatingSystem":"Web (all browsers)",
        "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"description":t["desc"]}]
    if t.get("faq"):
        rows = "".join(f'<h3 style="font-family:var(--serif);font-size:19px;color:var(--ink);margin:18px 0 4px">{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q,a in t["faq"])
        faq_html = f'<section style="margin-top:36px"><h2 style="font-family:var(--serif);font-size:24px;color:var(--ink);margin-bottom:8px">Questions</h2>{rows}</section>'
        schemas.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in t["faq"]]})
    schema_html = "".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schemas)
    # related tools strip
    others = [x for x in TOOLS if x["slug"] != t["slug"]]
    rel_cards = "".join(f'<a class="tcard" href="/tools/{x["slug"]}.html"><h3>{html.escape(x["h1"])}</h3><p>{html.escape(x["sub"])}</p></a>' for x in others)
    related = f'<section style="margin-top:40px"><h2 style="font-family:var(--serif);font-size:22px;color:var(--ink);margin-bottom:6px">More free tools</h2><div class="cards">{rel_cards}</div></section>'
    return ("""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ | Story Mode Guy</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="https://storymodeguy.com/tools/__SLUG__.html">
<link rel="icon" type="image/png" href="/smg-logo.png">
<meta property="og:title" content="__TITLE__"><meta property="og:description" content="__DESC__">
<meta property="og:url" content="https://storymodeguy.com/tools/__SLUG__.html"><meta property="og:image" content="https://storymodeguy.com/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>__CSS__</style>
__SCHEMA__</head><body>
__NAV__
<main class="wrap">
<div class="eyebrow">Free Tool</div>
<h1>__H1__</h1>
<div class="sub">__SUB__</div>
__BODY__
__CTA__
__FAQ__
__RELATED__
</main>
__FOOT__
</body></html>"""
        .replace("__CSS__", CSS.replace("__ACCENT__", t["accent"]))
        .replace("__NAV__", nav()).replace("__FOOT__", FOOT).replace("__SCHEMA__", schema_html)
        .replace("__TITLE__", html.escape(t["title"])).replace("__DESC__", html.escape(t["desc"]))
        .replace("__SLUG__", t["slug"]).replace("__H1__", html.escape(t["h1"]))
        .replace("__SUB__", html.escape(t["sub"])).replace("__BODY__", body).replace("__CTA__", cta)
        .replace("__FAQ__", faq_html).replace("__RELATED__", related))

TOOLS = [
{
 "slug":"golden-hour-calculator","accent":"#d97706",
 "title":"Golden Hour Calculator — Sunrise, Sunset & Blue Hour",
 "desc":"Find today's golden hour, blue hour, sunrise and sunset times for any location. Free, instant, no sign-up.",
 "h1":"Golden Hour Calculator","sub":"Sunrise, sunset, golden hour & blue hour for any spot — the best light of the day.",
 "cta_h":"Shoot the golden hour like a pro","cta_p":"The best light is worth planning for. Learn to expose and edit it beautifully.","cta_url":"/learn/04-exposure-manual-mode.html","cta_btn":"See the guide",
 "faq":[("What is the golden hour?","The golden hour is the roughly one-hour window just after sunrise and just before sunset, when the sun is low and the light is soft, warm, and directional — the most flattering natural light of the day."),
   ("What is the blue hour?","The blue hour is the short period before sunrise and after sunset when the sun is below the horizon and the sky glows deep blue. It's ideal for cityscapes, the boardwalk, and long-exposure water."),
   ("Are these times exact?","Sunrise and sunset are calculated precisely for your location and date. The golden and blue-hour windows are based on the sun's angle and are accurate to a few minutes — enough to plan a shoot.")],
 "body":"""<div class="tool">
<div class="row"><div><label>Latitude</label><input id="lat" type="number" step="0.0001" value="36.9741"></div>
<div><label>Longitude</label><input id="lng" type="number" step="0.0001" value="-122.0308"></div></div>
<label>Date</label><input id="date" type="date">
<div class="btnrow"><button class="act" id="geo">Use my location</button><button class="act" id="sc">Santa Cruz, CA</button></div>
<div class="out" id="out"></div>
<p class="note">Times use your device's time zone. Golden/blue-hour windows are based on the sun's angle above/below the horizon.</p>
</div>
<script>
function toMin(h){return h*60;}
function fmt(mins){if(mins==null||isNaN(mins))return "—";mins=((mins%1440)+1440)%1440;var h=Math.floor(mins/60),m=Math.round(mins-h*60);if(m===60){m=0;h++;}var ap=h<12?"AM":"PM";var hh=h%12;if(hh===0)hh=12;return hh+":"+(m<10?"0":"")+m+" "+ap;}
function rad(d){return d*Math.PI/180;}function deg(r){return r*180/Math.PI;}
// Returns local clock minutes for the sun reaching altitude `alt` deg, morning(rise=true)/evening.
function sunTime(date,lat,lng,alt,rise){
  var start=new Date(date.getFullYear(),0,0);var diff=date-start;var doy=Math.floor(diff/86400000);
  var lngHour=lng/15;var t=doy+((rise?6:18)-lngHour)/24;
  var M=(0.9856*t)-3.289;
  var L=M+(1.916*Math.sin(rad(M)))+(0.020*Math.sin(rad(2*M)))+282.634;L=(L+360)%360;
  var RA=deg(Math.atan(0.91764*Math.tan(rad(L))));RA=(RA+360)%360;
  var Lq=Math.floor(L/90)*90;var RAq=Math.floor(RA/90)*90;RA=(RA+(Lq-RAq))/15;
  var sinDec=0.39782*Math.sin(rad(L));var cosDec=Math.cos(Math.asin(sinDec));
  var cosH=(Math.sin(rad(alt))-(sinDec*Math.sin(rad(lat))))/(cosDec*Math.cos(rad(lat)));
  if(cosH>1||cosH<-1)return null;
  var H=rise?360-deg(Math.acos(cosH)):deg(Math.acos(cosH));H=H/15;
  var T=H+RA-(0.06571*t)-6.622;var UT=((T-lngHour)%24+24)%24;
  var localMin=UT*60 - (date.getTimezoneOffset());
  return localMin;
}
function calc(){
  var lat=parseFloat(document.getElementById('lat').value);var lng=parseFloat(document.getElementById('lng').value);
  var d=new Date(document.getElementById('date').value+"T12:00:00");
  if(isNaN(d.getTime())){d=new Date();}
  var sr=sunTime(d,lat,lng,-0.833,true),ss=sunTime(d,lat,lng,-0.833,false);
  var ghM_end=sunTime(d,lat,lng,6,true),ghE_start=sunTime(d,lat,lng,6,false);
  var bhM_start=sunTime(d,lat,lng,-6,true),bhE_end=sunTime(d,lat,lng,-6,false);
  document.getElementById('out').innerHTML=
   '<div class="grid2">'+
   '<div><div class="lab">Morning blue hour</div><div class="big">'+fmt(bhM_start)+'</div><div class="lab">to '+fmt(sr)+'</div></div>'+
   '<div><div class="lab">Sunrise</div><div class="big">'+fmt(sr)+'</div></div>'+
   '<div><div class="lab">Morning golden hour</div><div class="big">'+fmt(sr)+'</div><div class="lab">to '+fmt(ghM_end)+'</div></div>'+
   '<div><div class="lab">Evening golden hour</div><div class="big">'+fmt(ghE_start)+'</div><div class="lab">to '+fmt(ss)+'</div></div>'+
   '<div><div class="lab">Sunset</div><div class="big">'+fmt(ss)+'</div></div>'+
   '<div><div class="lab">Evening blue hour</div><div class="big">'+fmt(ss)+'</div><div class="lab">to '+fmt(bhE_end)+'</div></div>'+
   '</div>';
}
document.getElementById('date').valueAsDate=new Date();
document.getElementById('geo').onclick=function(){navigator.geolocation&&navigator.geolocation.getCurrentPosition(function(p){document.getElementById('lat').value=p.coords.latitude.toFixed(4);document.getElementById('lng').value=p.coords.longitude.toFixed(4);calc();});};
document.getElementById('sc').onclick=function(){document.getElementById('lat').value="36.9741";document.getElementById('lng').value="-122.0308";calc();};
['lat','lng','date'].forEach(function(id){document.getElementById(id).addEventListener('input',calc);});
calc();
</script>"""
},
{
 "slug":"long-exposure-nd-filter-calculator","accent":"#0e7490",
 "title":"Long Exposure & ND Filter Calculator",
 "desc":"Add an ND filter and get your new shutter speed instantly. Free long-exposure calculator for silky water and light trails.",
 "h1":"ND Filter & Long Exposure Calculator","sub":"Pick your base shutter and ND strength — get the corrected long-exposure time.",
 "cta_h":"Master long exposures","cta_p":"ND filters, the shutter rule, and the settings for silky water and light trails.","cta_url":"/learn/09-low-light-night.html","cta_btn":"See the guide",
 "body":"""<div class="tool">
<label>Base shutter speed (without filter)</label>
<select id="base"></select>
<label>ND filter strength</label>
<select id="nd">
<option value="1">ND2 (1 stop)</option><option value="2">ND4 (2 stops)</option><option value="3">ND8 (3 stops)</option>
<option value="4">ND16 (4 stops)</option><option value="6" selected>ND64 (6 stops)</option><option value="10">ND1000 (10 stops)</option>
<option value="15">ND32000 (15 stops)</option><option value="20">ND1M (20 stops)</option></select>
<div class="out"><div class="lab">New shutter time</div><div class="big" id="res">—</div><div class="note" id="tip"></div></div>
</div>
<script>
var speeds=[["1/8000",1/8000],["1/4000",1/4000],["1/2000",1/2000],["1/1000",1/1000],["1/500",1/500],["1/250",1/250],["1/125",1/125],["1/60",1/60],["1/30",1/30],["1/15",1/15],["1/8",1/8],["1/4",1/4],["1/2",0.5],["1s",1],["2s",2],["4s",4],["8s",8],["15s",15],["30s",30]];
var b=document.getElementById('base');speeds.forEach(function(s,i){var o=document.createElement('option');o.value=s[1];o.textContent=s[0];if(s[0]==="1/125")o.selected=true;b.appendChild(o);});
function human(sec){if(sec<1)return "1/"+Math.round(1/sec)+" sec";if(sec<60)return sec.toFixed(sec<10?1:0)+" sec";var m=Math.floor(sec/60),s=Math.round(sec-m*60);return m+" min "+(s?s+" sec":"");}
function calc(){var base=parseFloat(b.value);var stops=parseFloat(document.getElementById('nd').value);var t=base*Math.pow(2,stops);
document.getElementById('res').textContent=human(t);
document.getElementById('tip').textContent=t>=1?"Use a tripod and a remote or 2-sec timer. For times over 30s, switch to Bulb mode.":"Fast enough to hand-hold, but a tripod still sharpens it.";}
b.onchange=calc;document.getElementById('nd').onchange=calc;calc();
</script>"""
},
{
 "slug":"exposure-calculator","accent":"#7c2d12",
 "title":"Exposure Calculator — Equivalent Settings",
 "desc":"Change aperture, shutter, or ISO and see the equivalent exposures that keep the same brightness. Free exposure triangle tool.",
 "h1":"Equivalent Exposure Calculator","sub":"Change one setting and see how to trade the others to keep the same brightness.",
 "cta_h":"Finally understand the exposure triangle","cta_p":"Aperture, shutter, and ISO — what each does and how to trade them, in plain English.","cta_url":"/learn/04-exposure-manual-mode.html","cta_btn":"See the guide",
 "body":"""<div class="tool">
<div class="row"><div><label>Aperture (f/)</label><select id="ap"></select></div>
<div><label>Shutter</label><select id="sh"></select></div></div>
<label>ISO</label><select id="iso"></select>
<div class="out"><div class="lab">Total exposure value (relative)</div><div class="big" id="ev">—</div>
<div class="note">Adjust any control — the readout shows how many stops brighter or darker you've gone. To keep the same exposure, move another control the opposite number of stops.</div></div>
</div>
<script>
var aps=[1.4,2,2.8,4,5.6,8,11,16,22];var shs=[["1/2000",1/2000],["1/1000",1/1000],["1/500",1/500],["1/250",1/250],["1/125",1/125],["1/60",1/60],["1/30",1/30],["1/15",1/15],["1/8",1/8],["1/4",1/4],["1/2",0.5],["1s",1]];var isos=[100,200,400,800,1600,3200,6400];
function fill(id,arr,def,lab){var e=document.getElementById(id);arr.forEach(function(v){var o=document.createElement('option');if(lab){o.value=v[1];o.textContent=v[0];}else{o.value=v;o.textContent=(id==='ap'?'f/':'')+v;}if((lab?v[1]:v)==def)o.selected=true;e.appendChild(o);});}
fill('ap',aps,8);fill('sh',shs,1/125,true);fill('iso',isos,100);
var base=null;
function stops(){var ap=parseFloat(document.getElementById('ap').value);var sh=parseFloat(document.getElementById('sh').value);var iso=parseFloat(document.getElementById('iso').value);
// EV relative: brighter = lower f, longer shutter, higher iso
var ev=Math.log2(sh/(1/125))+Math.log2((8*8)/(ap*ap))+Math.log2(iso/100);return ev;}
function calc(){var ev=stops();if(base===null)base=ev;var d=ev-base;var s=Math.round(d*10)/10;
document.getElementById('ev').textContent=(s>0?"+":"")+s+" stop"+(Math.abs(s)===1?"":"s")+(s===0?" (reference)":(s>0?" brighter":" darker"));}
['ap','sh','iso'].forEach(function(id){document.getElementById(id).onchange=calc;});calc();
</script>"""
},
{
 "slug":"shutter-angle-frame-rate-calculator","accent":"#6d28d9",
 "title":"Shutter Speed for Video — 180° Rule Calculator",
 "desc":"Get the right shutter speed for your frame rate using the 180-degree rule — the key to natural, cinematic motion in video.",
 "h1":"Video Shutter Speed (180° Rule)","sub":"Pick your frame rate — get the shutter speed that gives natural, cinematic motion blur.",
 "cta_h":"Make your video look cinematic","cta_p":"Frame rate, the shutter rule, ND filters, and the settings that kill the home-video look.","cta_url":"/learn/v01-cinematic-look.html","cta_btn":"See the guide",
 "body":"""<div class="tool">
<label>Frame rate (fps)</label>
<select id="fps"><option>24</option><option>25</option><option selected>30</option><option>48</option><option>60</option><option>120</option></select>
<div class="out"><div class="lab">Shutter speed (180° rule)</div><div class="big" id="res">—</div>
<div class="note" id="tip"></div></div>
</div>
<script>
function nearest(x){var std=[1/24,1/25,1/30,1/48,1/50,1/60,1/96,1/100,1/120,1/240];var best=std[0];std.forEach(function(s){if(Math.abs(s-x)<Math.abs(best-x))best=s;});return best;}
function calc(){var fps=parseFloat(document.getElementById('fps').value);var ideal=1/(fps*2);var n=nearest(ideal);
document.getElementById('res').textContent="1/"+Math.round(1/n)+" sec";
document.getElementById('tip').textContent="At "+fps+" fps, set shutter to about 1/"+Math.round(1/n)+"s (2× the frame rate). In bright light you'll need an ND filter to keep it there. For slow-motion, shoot "+fps+" fps and play back at 24-30 fps.";}
document.getElementById('fps').onchange=calc;calc();
</script>"""
},
{
 "slug":"drone-preflight-checklist","accent":"#0284c7",
 "title":"Drone Pre-Flight Checklist (Free, Printable)",
 "desc":"A free interactive pre-flight checklist for drone pilots — run it before every flight to avoid crashes and flyaways. Saves your progress.",
 "h1":"Drone Pre-Flight Checklist","sub":"Run this before every flight. Most crashes and flyaways are prevented on the ground.",
 "cta_h":"Fly safe, stay legal, get the shot","cta_p":"The complete drone library — flying, laws & Part 107, cinematic moves, safety, and more.","cta_url":"/learn/d01-drone-beginners.html","cta_btn":"See the drone guides",
 "body":"""<div class="tool">
<ul class="check" id="list"></ul>
<div class="btnrow"><button class="act" id="reset">Reset</button><button class="act" id="print">Print checklist</button></div>
<p class="note">Your ticks are saved on this device. This is a general checklist — always follow your drone's manual and local aviation rules (in the US, the FAA). Verify airspace before you fly.</p>
</div>
<script>
var items=["Firmware & app updated","Propellers checked — no nicks or cracks","Batteries fully charged (drone + controller)","microSD card in, formatted, space free","Home point set & enough GPS satellites","Compass/IMU calibrated if prompted","Return-to-Home altitude set above tallest obstacle","Weather & wind within your drone's limit","Airspace checked — legal & clear to fly","Visual line of sight & a clear takeoff/landing spot","Camera settings dialed (ND, shutter, WB)","Gimbal clear & lens clean"];
var KEY="smg_drone_preflight";var state=JSON.parse(localStorage.getItem(KEY)||"{}");
var list=document.getElementById('list');
items.forEach(function(t,i){var li=document.createElement('li');var cb=document.createElement('input');cb.type='checkbox';cb.checked=!!state[i];if(state[i])li.className='done';
cb.onchange=function(){state[i]=cb.checked;li.className=cb.checked?'done':'';localStorage.setItem(KEY,JSON.stringify(state));};
var sp=document.createElement('span');sp.textContent=t;li.appendChild(cb);li.appendChild(sp);list.appendChild(li);});
document.getElementById('reset').onclick=function(){state={};localStorage.removeItem(KEY);document.querySelectorAll('#list input').forEach(function(c){c.checked=false;c.parentNode.className='';});};
document.getElementById('print').onclick=function(){window.print();};
</script>"""
},
{
 "slug":"depth-of-field-calculator","accent":"#9333ea",
 "title":"Depth of Field Calculator","desc":"Calculate depth of field, near/far focus limits and hyperfocal distance for any camera, lens and aperture. Free DoF calculator, no sign-up.",
 "h1":"Depth of Field Calculator","sub":"How much will be in focus? Set your camera, focal length, aperture and focus distance.",
 "cta_h":"Take control of focus and sharpness","cta_p":"Aperture, focus, and the settings for exactly the depth of field you want.","cta_url":"/learn/04-exposure-manual-mode.html","cta_btn":"See the guide",
 "body":"""<div class="tool">
<label>Camera / sensor</label>
<select id="crop"><option value="1">Full frame (1.0×)</option><option value="1.5">APS-C (1.5×)</option><option value="1.6">Canon APS-C (1.6×)</option><option value="2">Micro 4/3 (2.0×)</option><option value="2.7">1-inch (2.7×)</option></select>
<div class="row"><div><label>Focal length (mm)</label><input id="focal" type="number" value="50"></div>
<div><label>Aperture (f/)</label><input id="fnum" type="number" step="0.1" value="2.8"></div></div>
<label>Focus distance (meters)</label><input id="dist" type="number" step="0.1" value="3">
<div class="out"><div class="grid2">
<div><div class="lab">Near limit</div><div class="big" id="near">—</div></div>
<div><div class="lab">Far limit</div><div class="big" id="far">—</div></div>
<div><div class="lab">Total in focus</div><div class="big" id="total">—</div></div>
<div><div class="lab">Hyperfocal distance</div><div class="big" id="hyp">—</div></div>
</div><div class="note">Focus at the hyperfocal distance to keep everything from half that distance to infinity sharp.</div></div>
</div>
<script>
function m(x){if(!isFinite(x))return "∞";if(x<1)return (x*100).toFixed(0)+" cm";return x.toFixed(x<10?2:1)+" m";}
function calc(){var crop=parseFloat(document.getElementById('crop').value);var f=parseFloat(document.getElementById('focal').value);var N=parseFloat(document.getElementById('fnum').value);var s=parseFloat(document.getElementById('dist').value)*1000;
var coc=0.03/crop;var H=(f*f)/(N*coc)+f;
var near=(H*s)/(H+(s-f));var far=(s<H)?(H*s)/(H-(s-f)):Infinity;
var total=isFinite(far)?(far-near):Infinity;
document.getElementById('near').textContent=m(near/1000);document.getElementById('far').textContent=m(far/1000);
document.getElementById('total').textContent=m(total/1000);document.getElementById('hyp').textContent=m(H/1000);}
['crop','focal','fnum','dist'].forEach(function(id){document.getElementById(id).addEventListener('input',calc);});calc();
</script>"""
},
{
 "slug":"handheld-shutter-speed-calculator","accent":"#9f1239",
 "title":"Handheld Shutter Speed Calculator (Reciprocal Rule)","desc":"Find the slowest shutter speed for sharp handheld photos using the reciprocal rule, adjusted for your sensor and image stabilization.",
 "h1":"Handheld Shutter Speed","sub":"The slowest shutter you can hand-hold sharp — from your focal length, sensor and stabilization.",
 "cta_h":"Never take a blurry photo again","cta_p":"Diagnose the three kinds of blur and fix each one — the complete sharpness guide.","cta_url":"/learn/05-why-blurry.html","cta_btn":"See the guide",
 "body":"""<div class="tool">
<div class="row"><div><label>Focal length (mm)</label><input id="focal" type="number" value="50"></div>
<div><label>Sensor</label><select id="crop"><option value="1">Full frame</option><option value="1.5">APS-C (1.5×)</option><option value="1.6">Canon APS-C</option><option value="2">Micro 4/3</option></select></div></div>
<label>Image stabilization</label>
<select id="is"><option value="0">None</option><option value="2">Basic (2 stops)</option><option value="4">Good (4 stops)</option><option value="6">Excellent (6 stops)</option></select>
<div class="out"><div class="lab">Slowest safe shutter</div><div class="big" id="res">—</div>
<div class="note" id="tip"></div></div>
</div>
<script>
function nearestSh(sec){var std=[1/4000,1/2000,1/1000,1/500,1/250,1/125,1/60,1/30,1/15,1/8,1/4,1/2,1,2,4];var best=std[0];std.forEach(function(s){if(s<=sec)best=s;});return best;}
function lab(sec){if(sec<1)return "1/"+Math.round(1/sec)+" sec";return sec+" sec";}
function calc(){var f=parseFloat(document.getElementById('focal').value);var crop=parseFloat(document.getElementById('crop').value);var is=parseFloat(document.getElementById('is').value);
var equiv=f*crop;var base=1/equiv;var allowed=base*Math.pow(2,is);var pick=nearestSh(allowed);
document.getElementById('res').textContent=lab(pick)+" or faster";
document.getElementById('tip').textContent="At "+f+"mm on this sensor (≈"+Math.round(equiv)+"mm equivalent), the reciprocal rule says 1/"+Math.round(equiv)+"s"+(is>0?", and your "+is+"-stop stabilization buys you down to about "+lab(pick):"")+". For moving subjects, go faster regardless.";}
['focal','crop','is'].forEach(function(id){document.getElementById(id).addEventListener('input',calc);document.getElementById(id).addEventListener('change',calc);});calc();
</script>"""
},
{
 "slug":"time-lapse-calculator","accent":"#0891b2",
 "title":"Time-Lapse Calculator","desc":"Work out your time-lapse shooting interval, number of shots, and how long you need to shoot for a clip of any length. Free, no sign-up.",
 "h1":"Time-Lapse Calculator","sub":"Plan a time-lapse: set the interval and target clip length — get shots needed and shooting time.",
 "cta_h":"Shoot smooth, cinematic time-lapses","cta_p":"Settings, intervals, and the editing workflow for time-lapse and hyperlapse.","cta_url":"/learn/v01-cinematic-look.html","cta_btn":"See the guide",
 "faq":[("What interval should I use for a time-lapse?","Slow scenes like sunsets or stars: 5–30 seconds between shots. Faster action like clouds or crowds: 1–3 seconds. Very fast subjects like traffic: 1 second or less."),
   ("How long do I need to shoot?","Shooting time = interval × (clip length in seconds × output fps). This calculator does the math for you — a 10-second clip at 30fps needs 300 frames, so at a 3-second interval that's 15 minutes of shooting.")],
 "body":"""<div class="tool">
<div class="row"><div><label>Interval between shots (sec)</label><input id="int" type="number" step="0.5" value="3"></div>
<div><label>Output frame rate (fps)</label><select id="fps"><option>24</option><option selected>30</option><option>60</option></select></div></div>
<label>Desired final clip length (seconds)</label><input id="len" type="number" value="10">
<div class="out"><div class="grid2">
<div><div class="lab">Frames (shots) needed</div><div class="big" id="shots">—</div></div>
<div><div class="lab">Total shooting time</div><div class="big" id="dur">—</div></div>
</div><div class="note" id="tip"></div></div>
</div>
<script>
function hms(s){var h=Math.floor(s/3600),m=Math.floor((s%3600)/60),ss=Math.round(s%60);var o=[];if(h)o.push(h+"h");if(m)o.push(m+"m");o.push(ss+"s");return o.join(" ");}
function calc(){var i=parseFloat(document.getElementById('int').value);var fps=parseFloat(document.getElementById('fps').value);var len=parseFloat(document.getElementById('len').value);
var shots=Math.round(len*fps);var dur=shots*i;
document.getElementById('shots').textContent=shots.toLocaleString();document.getElementById('dur').textContent=hms(dur);
document.getElementById('tip').textContent="At a "+i+"s interval you'll capture "+shots.toLocaleString()+" frames over "+hms(dur)+" to make a "+len+"s clip at "+fps+"fps. Bring enough battery and card space.";}
['int','fps','len'].forEach(function(id){document.getElementById(id).addEventListener('input',calc);document.getElementById(id).addEventListener('change',calc);});calc();
</script>"""
},
{
 "slug":"crop-factor-calculator","accent":"#4338ca",
 "title":"Crop Factor & Equivalent Focal Length Calculator","desc":"Convert any lens to its full-frame equivalent focal length and see the effective aperture for your sensor. Free crop factor calculator.",
 "h1":"Crop Factor Calculator","sub":"See the full-frame-equivalent focal length and depth-of-field aperture for your camera.",
 "cta_h":"Understand your gear","cta_p":"Focal length, aperture, and how your sensor changes the look — made simple.","cta_url":"/learn/04-exposure-manual-mode.html","cta_btn":"See the guide",
 "faq":[("What is crop factor?","Crop factor compares your sensor to full frame (35mm). A smaller sensor 'crops' the view, so a lens acts like a longer one. Multiply the focal length by the crop factor to get the full-frame-equivalent field of view."),
   ("Does crop factor change my aperture?","It doesn't change exposure, but it does change depth of field. For an equivalent look, multiply the aperture by the crop factor too — f/2.8 on Micro 4/3 gives roughly the depth of field of f/5.6 on full frame.")],
 "body":"""<div class="tool">
<div class="row"><div><label>Sensor</label><select id="crop"><option value="1">Full frame (1.0×)</option><option value="1.5" selected>APS-C (1.5×)</option><option value="1.6">Canon APS-C (1.6×)</option><option value="2">Micro 4/3 (2.0×)</option><option value="2.7">1-inch (2.7×)</option></select></div>
<div><label>Focal length (mm)</label><input id="focal" type="number" value="35"></div></div>
<label>Aperture (f/)</label><input id="fnum" type="number" step="0.1" value="1.8">
<div class="out"><div class="grid2">
<div><div class="lab">Equivalent focal length</div><div class="big" id="ef">—</div></div>
<div><div class="lab">Equivalent depth-of-field aperture</div><div class="big" id="ea">—</div></div>
</div><div class="note">Same field of view and depth-of-field look as this on a full-frame camera.</div></div>
</div>
<script>
function calc(){var c=parseFloat(document.getElementById('crop').value);var f=parseFloat(document.getElementById('focal').value);var a=parseFloat(document.getElementById('fnum').value);
document.getElementById('ef').textContent=Math.round(f*c)+" mm";document.getElementById('ea').textContent="f/"+(a*c).toFixed(1);}
['crop','focal','fnum'].forEach(function(id){document.getElementById(id).addEventListener('input',calc);document.getElementById(id).addEventListener('change',calc);});calc();
</script>"""
},
{
 "slug":"print-size-calculator","accent":"#b45309",
 "title":"Photo Print Size Calculator (Megapixels to Print)","desc":"Find the biggest sharp print you can make from your photo's megapixels at 300, 240, and 150 DPI. Free print size calculator.",
 "h1":"Print Size Calculator","sub":"How big can you print? Enter your image's pixel dimensions or megapixels.",
 "cta_h":"Make prints worth hanging","cta_p":"Shoot, edit, and export for beautiful fine-art prints.","cta_url":"/learn/02-lightroom-blueprint.html","cta_btn":"See the guide",
 "faq":[("What DPI do I need for a print?","300 DPI is the standard for sharp prints viewed up close (photo books, small prints). 240 DPI is excellent for most wall prints. 150 DPI is fine for large prints viewed from a distance, like posters."),
   ("How many megapixels do I need to print big?","At 300 DPI, a 24-megapixel image prints beautifully to about 13×20 inches. For larger prints you rely on normal viewing distance — a 24MP file makes a great 24×36 poster at ~150 DPI.")],
 "body":"""<div class="tool">
<div class="row"><div><label>Image width (pixels)</label><input id="w" type="number" value="6000"></div>
<div><label>Image height (pixels)</label><input id="h" type="number" value="4000"></div></div>
<div class="out"><div class="lab" id="mp"></div>
<div class="grid2" style="margin-top:8px">
<div><div class="lab">At 300 DPI (gallery)</div><div class="big" id="d300">—</div></div>
<div><div class="lab">At 240 DPI (wall)</div><div class="big" id="d240">—</div></div>
<div><div class="lab">At 150 DPI (poster)</div><div class="big" id="d150">—</div></div>
</div></div>
</div>
<script>
function sz(w,h,dpi){return (w/dpi).toFixed(1)+" × "+(h/dpi).toFixed(1)+" in";}
function calc(){var w=parseFloat(document.getElementById('w').value);var h=parseFloat(document.getElementById('h').value);
document.getElementById('mp').textContent=((w*h)/1e6).toFixed(1)+" megapixels";
document.getElementById('d300').textContent=sz(w,h,300);document.getElementById('d240').textContent=sz(w,h,240);document.getElementById('d150').textContent=sz(w,h,150);}
['w','h'].forEach(function(id){document.getElementById(id).addEventListener('input',calc);});calc();
</script>"""
},
]

for t in TOOLS:
    (OUT / f"{t['slug']}.html").write_text(shell(t))
    print("  wrote tools/"+t["slug"]+".html")

# index
cards="".join(f'<a class="tcard" href="/tools/{t["slug"]}.html"><h3>{html.escape(t["h1"])}</h3><p>{html.escape(t["sub"])}</p></a>' for t in TOOLS)
idx=("""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Free Photography, Video & Drone Tools | Story Mode Guy</title>
<meta name="description" content="Free calculators for photographers and filmmakers — golden hour, ND filters, exposure, video shutter speed, and a drone pre-flight checklist.">
<link rel="canonical" href="https://storymodeguy.com/tools/">
<link rel="icon" type="image/png" href="/smg-logo.png">
<meta property="og:title" content="Free Photography, Video & Drone Tools"><meta property="og:image" content="https://storymodeguy.com/og-image.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>__CSS__</style></head><body>
__NAV__
<main class="wrap"><div class="eyebrow">Free Tools</div><h1>Free tools for photographers &amp; filmmakers</h1>
<div class="sub">Handy calculators — no sign-up, no ads. Bookmark them.</div>
<div class="cards">__CARDS__</div></main>
__FOOT__</body></html>""".replace("__CSS__",CSS.replace("__ACCENT__","#41a1cf")).replace("__NAV__",nav()).replace("__FOOT__",FOOT).replace("__CARDS__",cards))
(OUT/"index.html").write_text(idx)
print("  wrote tools/index.html")

# sitemap
sm=ROOT/"sitemap.xml"
if sm.exists():
    s=sm.read_text();urls=["https://storymodeguy.com/tools/"]+[f"https://storymodeguy.com/tools/{t['slug']}.html" for t in TOOLS]
    add="".join(f'  <url>\n    <loc>{u}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n\n' for u in urls if u not in s)
    if add: s=s.replace("</urlset>",add+"</urlset>",1);sm.write_text(s);print("  sitemap +%d"%add.count("<url>"))
print("done")
