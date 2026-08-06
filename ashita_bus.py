from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
SITE_URL = "https://anobus.jp/"


def image_data_uri(filename: str) -> str:
    path = ASSETS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"画像が見つかりません: {path}")
    suffix = path.suffix.lower()
    mime = "image/jpeg" if suffix in {".jpg", ".jpeg"} else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def load_assets() -> dict[str, str]:
    files = {
        "logo": "logo.png",
        "bus": "bus.png",
        "dog": "dog.png",
        "cat": "cat.png",
        "usagi": "usagi.png",
        "usagi2": "usagi2.png",
        "women": "women.png",
        "city": "city-background.png",
        "castle": "castle.png",
        "fuji": "fuji.png",
        "sattue": "sattue.png",
        "tokyo_tower": "tokyo-tower.png",
        "tower": "tower.png",
        "interior": "photo_bus_interior.JPG",
    }
    return {key: image_data_uri(filename) for key, filename in files.items()}


def streamlit_shell_css() -> None:
    st.markdown(
        """
        <style>
        header, footer, #MainMenu,
        [data-testid="stHeader"], [data-testid="stSidebar"],
        [data-testid="stToolbar"], [data-testid="stDecoration"] {
            display: none !important;
        }
        html, body, [data-testid="stAppViewContainer"] {
            margin: 0 !important;
            padding: 0 !important;
            background: #dff5ff !important;
        }
        .block-container {
            max-width: 100% !important;
            padding: 0 !important;
        }
        iframe {
            display: block;
            width: 100%;
            border: 0;
        }
        

</style>
        """,
        unsafe_allow_html=True,
    )


def build_html(assets: dict[str, str]) -> str:
    a = {key: html.escape(value, quote=True) for key, value in assets.items()}
    template = r'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>あしたのバス｜ナイトライナー車内Wi-Fi</title>
<style>
:root{
  --blue:#165fe3;
  --deep:#0b265a;
  --sky:#72d1f1;
  --sky-pale:#e9f8ff;
  --yellow:#ffe14f;
  --pink:#ff6f9e;
  --green:#71d7b4;
  --orange:#ffad48;
  --white:#fff;
  --rail:28px;
  --max:480px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;background:#dff5ff}
body{margin:0;background:#dff5ff;color:var(--deep);font-family:"Hiragino Kaku Gothic ProN","Yu Gothic","YuGothic",Meiryo,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow-x:hidden;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
a{text-decoration:none;color:inherit}
button{font:inherit}
.lp{position:relative;width:min(100%,var(--max));margin:0 auto;background:#f7fcff;box-shadow:0 0 45px rgba(28,70,118,.16);overflow-x:clip;overflow-y:visible}
.section{position:relative;min-height:100svh;overflow:hidden;isolation:isolate}
.inner{position:relative;z-index:5}
.reveal{opacity:0;transform:translateY(26px);transition:opacity .8s cubic-bezier(.2,.75,.2,1),transform .8s cubic-bezier(.2,.75,.2,1)}
.reveal.show{opacity:1;transform:none}

/* 1. Reality / first view: scroll toward the light */
.hero{height:188svh;background:#061326;color:#fff;overflow:visible}
.hero-stage{position:sticky;position:-webkit-sticky;top:0;height:100dvh;min-height:100dvh;overflow:hidden;background:#061326;z-index:1}
.hero-photo{position:absolute;inset:-3%;background-image:linear-gradient(rgba(3,13,30,.10),rgba(3,13,30,.28)),url('__INTERIOR__');background-size:cover;background-position:center center;transform:scale(1.02);transform-origin:50% 30%;will-change:transform,filter,opacity}
.hero-photo:after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 28%,rgba(255,255,255,.18),transparent 22%),linear-gradient(180deg,rgba(0,0,0,0),rgba(2,15,34,.18));pointer-events:none}
.hero-light{position:absolute;z-index:1;left:50%;top:28%;width:34%;height:13%;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,1) 0%,rgba(221,249,255,.9) 25%,rgba(255,255,255,0) 72%);filter:blur(13px);opacity:.38;animation:breatheLight 3.2s ease-in-out infinite;will-change:transform,opacity}
@keyframes breatheLight{50%{opacity:.62;transform:translate(-50%,-50%) scale(1.14)}}
.hero-whiteout{position:absolute;z-index:2;inset:-8%;background:radial-gradient(circle at 50% 30%,#fff 0 10%,rgba(236,250,255,.98) 30%,rgba(202,239,250,.92) 68%,#8fdcf6 100%);opacity:0;pointer-events:none;will-change:opacity}
.hero-world{position:absolute;z-index:3;inset:0;opacity:0;pointer-events:none;overflow:hidden;background:linear-gradient(180deg,#effcff 0%,#a6e4f7 56%,#73d2f2 100%);will-change:opacity}
.hero-world:before{content:"";position:absolute;left:50%;top:25%;width:78%;height:48%;transform:translate(-50%,-50%) scale(.45);border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,1) 0 11%,rgba(241,252,255,.95) 30%,rgba(154,225,246,.55) 58%,rgba(115,210,242,0) 78%);filter:blur(4px);opacity:0;will-change:transform,opacity}
.hero-world-road{position:absolute;left:-8%;right:-8%;bottom:8.5svh;height:68px;background:#f9fbfd;border-top:3px solid #d9e7ef;border-bottom:3px solid #d9e7ef}
.hero-world-road:after{content:"";position:absolute;left:0;right:0;top:50%;height:3px;background:repeating-linear-gradient(90deg,#a8bfd0 0 24px,transparent 24px 48px)}
.hero-world-bus{position:absolute;z-index:3;left:50%;top:27%;width:152px;opacity:0;transform:translate(-50%,-50%) scale(.12);filter:drop-shadow(0 13px 17px rgba(17,63,105,.22));will-change:left,top,transform,opacity}
.hero-world-bubble{
position:absolute;
z-index:4;
left:50%;
bottom:25svh;
min-width:150px;
padding:13px 18px 14px;
border:3px solid var(--deep);
border-radius:24px;
background:#fff;
color:var(--deep);
font-size:19px;
line-height:1.28;
font-weight:950;
text-align:center;
box-shadow:7px 7px 0 var(--yellow);
opacity:0;
transform:translate(-50%,8px) scale(.9);
transform-origin:50% 100%;
will-change:opacity,transform
}
.hero-world-bubble:after{
content:"";
position:absolute;
left:50%;
bottom:-12px;
width:20px;
height:20px;
margin-left:-10px;
background:#fff;
border-right:3px solid var(--deep);
border-bottom:3px solid var(--deep);
transform:rotate(45deg);
box-sizing:border-box
}

.hero-card{position:absolute;z-index:4;left:50%;top:34%;width:min(88%,390px);transform:translate(-50%,-50%);padding:20px 20px 22px;border:1px solid rgba(205,226,242,.92);border-radius:22px;background:linear-gradient(180deg,rgba(255,255,255,.98) 0%,rgba(255,255,255,.96) 72%,rgba(247,252,255,.94) 100%);color:var(--deep);text-align:center;box-shadow:0 18px 46px rgba(7,32,70,.16),inset 0 1px 0 rgba(255,255,255,1);backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px);will-change:transform,opacity;overflow:hidden}
.hero-card:before{content:"";position:absolute;left:0;right:0;top:0;height:5px;background:linear-gradient(90deg,#1767df,#59c8eb)}
.hero-official{display:inline-flex;align-items:center;justify-content:center;margin:2px auto 14px;padding:7px 13px;border-radius:999px;background:rgba(21,89,214,.09);color:#1559d6;font-size:11px;line-height:1;font-weight:800;letter-spacing:.08em}
.hero-logo{width:150px;margin:0 auto 18px}
.hero-card h1{width:100%;margin:0;font-family:"Hiragino Kaku Gothic ProN","Yu Gothic","YuGothic",Meiryo,sans-serif;font-size:clamp(29px,7vw,37px);line-height:1.2;letter-spacing:-.04em;font-weight:800;font-feature-settings:"palt" 1;word-break:keep-all;text-align:center;color:#102f63}
.hero-card h1 span{display:block;width:100%;white-space:nowrap}
.hero-card h1 .thanks{margin-top:4px}
.hero-card p{margin:13px 0 0;font-size:13px;line-height:1.85;font-weight:650;letter-spacing:.01em;color:#223b5d}
.hero-hook{position:absolute;z-index:5;left:50%;top:72dvh;bottom:auto;width:min(84%,320px);transform:translateX(-50%) translateY(14px);padding:13px 16px 9px;border:1px solid rgba(255,255,255,.24);border-radius:22px;background:linear-gradient(180deg,rgba(4,20,45,.20),rgba(4,20,45,.68));text-align:center;color:#fff;opacity:.42;will-change:opacity,transform;filter:drop-shadow(0 8px 18px rgba(0,0,0,.26));backdrop-filter:blur(5px)}
.hero-hook .hook-label{display:block;margin-bottom:7px;color:#a9dfff;font-size:11px;line-height:1;font-weight:800;letter-spacing:.12em}.hero-hook strong{display:block;font-size:16px;line-height:1.45;letter-spacing:.01em;font-weight:900;text-shadow:0 3px 16px rgba(0,0,0,.78)}
.hero-hook .chevron{display:block;margin-top:5px;font-size:32px;line-height:.8;font-weight:900;animation:chevron 1.7s ease-in-out infinite}
@keyframes chevron{0%,100%{transform:translateY(0);opacity:.55}50%{transform:translateY(8px);opacity:1}}

/* v69: cards are triggered directly by the visible reasons heading */
/* 2. White light becomes the pop world */
.portal{display:none}
.portal-glow{position:absolute;z-index:2;left:-18%;right:-18%;top:-24svh;height:48svh;background:radial-gradient(circle at 50% 34%,rgba(255,255,255,.98) 0 12%,rgba(223,248,255,.94) 30%,rgba(133,216,244,.82) 58%,rgba(117,210,242,0) 82%);transform:scale(.96);opacity:.88;pointer-events:none;transition:transform .7s ease,opacity .7s ease}
.portal.active .portal-glow{transform:scale(1.12);opacity:1}
.portal-copy{position:absolute;z-index:3;left:50%;top:49%;width:82%;transform:translate(-50%,-50%);text-align:center;color:var(--deep)}
.portal-copy p{margin:0;font-size:15px;line-height:1.8;font-weight:800;opacity:.72}
.portal-copy b{display:block;margin-top:8px;font-size:28px}

/* 3. Pop world rails */
.pop-world{position:relative;margin-top:-1px;background:linear-gradient(180deg,#77d3f3 0%,#dff6ff 18%,#fff 100%)}
.rail{position:fixed;z-index:80;top:0;bottom:0;width:var(--rail);background:#fff;overflow:hidden;pointer-events:none;opacity:0;transform:translateX(-120%);transition:opacity .7s ease,transform .7s ease;box-shadow:inset -2px 0 0 #3ab6e5,inset 2px 0 0 #3ab6e5}
.rail.right{right:max(calc((100vw - var(--max))/2),0px);transform:translateX(120%)}
.rail.left{left:max(calc((100vw - var(--max))/2),0px)}
.rail.show{opacity:1;transform:translateX(0)}
.rail-stack{height:100%;min-height:100%;display:flex;flex-direction:column;align-items:center;justify-content:space-around;gap:0;padding:8px 0;overflow:hidden}
.rail-slot{width:100%;min-height:78px;display:flex;align-items:center;justify-content:center;flex:1 1 0;overflow:hidden}
.rail-unit{width:62px;max-width:none;flex:0 0 auto;transform:rotate(90deg);transform-origin:center}
.pop-content{position:relative;width:calc(100% - var(--rail)*2);margin-left:var(--rail)}

/* 4. Question and comparison */
.compare-section{min-height:auto;padding:22px 20px 0;background:linear-gradient(180deg,#73d2f2 0%,#dff6ff 12%,#fff 34%,#fff 100%)}
.bus-intro{position:relative;min-height:188px;margin:0 auto 12px;max-width:350px;overflow:visible}
.intro-road{position:absolute;left:-18%;right:-18%;bottom:28px;height:52px;background:#f7f9fb;border-top:3px solid #d9e7ef;border-bottom:3px solid #d9e7ef;transform:rotate(-1deg)}
.intro-road:after{content:"";position:absolute;left:0;right:0;top:50%;height:3px;background:repeating-linear-gradient(90deg,#a8bfd0 0 24px,transparent 24px 45px)}
.intro-bus{position:absolute;z-index:3;left:0;bottom:42px;width:150px;opacity:0;transform:translateX(-150%) rotate(-2deg);filter:drop-shadow(0 12px 16px rgba(17,63,105,.2))}
.bus-intro.show .intro-bus{animation:introBusDrive 1.25s cubic-bezier(.18,.82,.25,1) .05s forwards}
@keyframes introBusDrive{0%{opacity:0;transform:translateX(-150%) rotate(-2deg)}72%{opacity:1;transform:translateX(82%) rotate(1deg)}100%{opacity:1;transform:translateX(74%) rotate(0)}}
.bus-bubble{position:absolute;z-index:5;right:12px;top:18px;padding:13px 21px;border:3px solid var(--deep);border-radius:24px;background:#fff;font-size:24px;font-weight:950;box-shadow:7px 7px 0 var(--yellow);opacity:0;transform:translateY(10px) scale(.96)}
.bus-intro.show .bus-bubble{animation:introBubble .48s ease .92s forwards}
@keyframes introBubble{to{opacity:1;transform:translateY(0) scale(1)}}
.bus-bubble:after{content:"";position:absolute;left:-13px;bottom:14px;width:22px;height:22px;background:#fff;border-left:3px solid var(--deep);border-bottom:3px solid var(--deep);transform:rotate(45deg)}
.question-title{
padding-right:12px;font-size:clamp(36px,10vw,48px);line-height:1.18;letter-spacing:-.045em;font-weight:950;color:var(--deep)}
.question-title .accent{position:relative;display:inline-block;color:var(--blue)}
.question-title .accent:after{content:"";position:absolute;z-index:-1;left:-3px;right:-4px;bottom:4px;height:12px;border-radius:99px;background:var(--yellow);transform:rotate(-1deg)}
.comparison{position:relative;margin-top:20px;padding-top:38px;filter:drop-shadow(0 18px 36px rgba(21,73,135,.14))}
.recommend-tag{position:absolute;z-index:8;top:-2px;left:39%;transform:translateX(-50%) rotate(-3deg) scale(1.04);padding:9px 17px;border-radius:999px;background:var(--yellow);color:var(--deep);font-size:12px;font-weight:950;box-shadow:5px 6px 0 rgba(255,111,158,.34),0 10px 24px rgba(255,193,46,.20)}
.compare-head{display:grid;grid-template-columns:64px 1.14fr 1fr 1fr;align-items:end}
.compare-head > div{min-height:76px;padding:13px 5px;display:grid;place-items:center;text-align:center;border-radius:14px 14px 0 0;background:#e8edf3;color:#344154;font-size:11px;line-height:1.35;font-weight:900}
.compare-head .blank{background:transparent}
.compare-head .ashita{position:relative;z-index:6;min-height:102px;background:linear-gradient(180deg,#3284ff 0%,#1559d6 100%);color:#fff;transform:translateY(-18px) scale(1.075);box-shadow:0 22px 44px rgba(22,95,227,.40),0 0 0 4px rgba(255,255,255,.75)}
.compare-grid{position:relative;display:grid;grid-template-columns:64px 1.14fr 1fr 1fr;border-radius:0 0 20px 20px;background:#fff;box-shadow:0 22px 48px rgba(25,59,105,.15);overflow:visible}
.cell{min-height:112px;padding:12px 6px;display:grid;place-items:center;text-align:center;border-right:1px solid #e1e7ee;border-bottom:1px solid #e1e7ee;font-size:10px;line-height:1.4;font-weight:750;color:#334154}
.cell.label{font-weight:950;color:var(--deep);background:#f4f9fd}
.label-wrap{display:grid;place-items:center;gap:8px}
.label-icon{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;font-size:18px}
.label-icon.price{background:#fff1a8}.label-icon.safe{background:#c9f4e6}.label-icon.seat{background:#cfefff}.label-icon.point{background:#ffd6e5}
.cell.ashita{position:relative;z-index:4;background:linear-gradient(180deg,#ffffff 0%,#eaf6ff 100%);color:var(--deep);font-weight:950;border-left:5px solid var(--blue);border-right:5px solid var(--blue);box-shadow:0 12px 28px rgba(22,95,227,.14)}
.cell.ashita.first{border-top:4px solid var(--blue)}
.cell.ashita.last{border-bottom:4px solid var(--blue);border-radius:0 0 16px 16px}
.cell strong{display:block;margin-bottom:5px;color:var(--pink);font-size:16px;line-height:1.15;text-shadow:0 2px 0 #fff}
.mark{display:block;margin-top:8px;font-size:27px;line-height:1}.good{color:var(--blue)}.mid{color:#f2a312}.bad{color:#8b97a4}
.column-glow{position:absolute;z-index:5;left:64px;top:0;width:calc((100% - 64px)*.363);height:100%;pointer-events:none;border-radius:18px;box-shadow:0 0 0 5px rgba(22,95,227,.98),0 0 38px rgba(255,111,158,.40),0 22px 44px rgba(22,95,227,.18);transform:translateY(-12px) scale(1.025);animation:highlight 2.25s ease-in-out infinite}
@keyframes highlight{50%{box-shadow:0 0 0 4px rgba(22,95,227,1),0 0 38px rgba(255,111,158,.48)}}


.question-block{position:relative;margin:-10px 0 34px}
.question-title{
margin:0;
width:100%;
text-align:left;
word-break:keep-all;
overflow-wrap:normal;
opacity:0;
transform:translateY(24px) scale(.96);
filter:blur(4px);
transition:
  opacity .72s cubic-bezier(.2,.8,.2,1),
  transform .72s cubic-bezier(.2,.8,.2,1),
  filter .72s ease;
}
.question-block.show .question-title{
opacity:1;
transform:none;
filter:none;
}
.question-title .line{
display:block;
opacity:0;
transform:translateY(16px);
}

.question-title .line{
  width:100%;
  white-space:normal;
}
.question-title .line-1{
  font-size:clamp(30px,8.1vw,39px);
}
.question-title .line-2{
  font-size:clamp(30px,8.1vw,39px);
}
.question-title .line-3{
  font-size:clamp(24px,6.35vw,31px);
  letter-spacing:-.07em;
  padding-right:10px;
}

.question-block.show .question-title .line:nth-child(1){animation:questionLineIn .58s cubic-bezier(.18,.9,.28,1.08) .02s forwards}
.question-block.show .question-title .line:nth-child(2){animation:questionLineIn .58s cubic-bezier(.18,.9,.28,1.08) .17s forwards}
.question-block.show .question-title .line:nth-child(3){animation:questionLineIn .66s cubic-bezier(.18,.92,.28,1.14) .34s forwards}
@keyframes questionLineIn{
0%{opacity:0;transform:translateY(24px) scale(.94);filter:blur(5px)}
68%{opacity:1;transform:translateY(-3px) scale(1.025);filter:blur(0)}
100%{opacity:1;transform:none;filter:none}
}
.question-title .accent{
display:inline-block;
transform-origin:center bottom;
}
.question-block.show .question-title .accent{
animation:questionAccentPop .48s cubic-bezier(.18,.9,.28,1.25) .42s both;
}
@keyframes questionAccentPop{
0%{transform:scale(.92);opacity:.25}
65%{transform:scale(1.04);opacity:1}
100%{transform:scale(1)}
}


.question-answer{
  position:relative;
  display:flex;
  align-items:flex-end;
  gap:10px;
  margin-top:18px;
  opacity:0;
  transform:translateY(14px) scale(.98);
  transition:
    opacity .54s ease .42s,
    transform .54s cubic-bezier(.2,.82,.2,1) .42s;
}
.question-block.show .question-answer{
  opacity:1;
  transform:none;
}
.answer-kicker{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding:5px 10px;
  border-radius:999px;
  background:var(--yellow);
  color:var(--deep);
  font-size:12px;
  line-height:1;
  font-weight:900;
  box-shadow:3px 3px 0 rgba(255,111,158,.18);
  transform-origin:left center;
}
.question-block.show .answer-kicker{
  animation:answerPop .5s cubic-bezier(.18,.9,.28,1.25) .58s both;
}
@keyframes answerPop{
  0%{transform:scale(.82) rotate(-2deg);opacity:0}
  70%{transform:scale(1.05) rotate(1deg);opacity:1}
  100%{transform:scale(1) rotate(0)}
}
.question-answer p{
  margin:10px 0 0;
  color:#17366e;
  font-size:clamp(16px,4.4vw,19px);
  line-height:1.62;
  letter-spacing:-.02em;
  font-weight:800;
}
.question-answer p span{
  display:block;
  opacity:0;
  transform:translateY(12px);
}
.question-block.show .question-answer p span:nth-child(1){
  animation:answerLineIn .46s ease .72s forwards;
}
.question-block.show .question-answer p span:nth-child(2){
  animation:answerLineIn .52s ease .88s forwards;
}
@keyframes answerLineIn{
  to{opacity:1;transform:none}
}



@keyframes answerGuide{
  0%,100%{transform:scaleY(.65);opacity:.35}
  50%{transform:scaleY(1);opacity:1}
}


.answer-cat{
  flex:0 0 auto;
  width:72px;
  max-height:88px;
  object-fit:contain;
  filter:drop-shadow(0 8px 12px rgba(15,53,101,.14));
  opacity:0;
  transform:translateX(-12px) scale(.92);
}
.question-block.show .answer-cat{
  animation:catTalkIn .56s cubic-bezier(.18,.9,.28,1.18) .46s forwards;
}
@keyframes catTalkIn{
  to{opacity:1;transform:none}
}
.answer-bubble{
  position:relative;
  flex:1;
  padding:13px 15px 14px;
  border-radius:19px;
  background:rgba(255,255,255,.94);
  border:2px solid rgba(22,95,227,.13);
  box-shadow:0 10px 24px rgba(22,95,227,.09);
}
.answer-bubble:before{
  content:"";
  position:absolute;
  left:-10px;
  bottom:20px;
  width:18px;
  height:18px;
  background:#fff;
  border-left:2px solid rgba(22,95,227,.13);
  border-bottom:2px solid rgba(22,95,227,.13);
  transform:rotate(45deg);
}
.answer-bubble:after{
  content:"";
  display:block;
  width:2px;
  height:22px;
  margin:10px auto -4px;
  background:linear-gradient(180deg,rgba(22,95,227,.06),rgba(22,95,227,.62));
  border-radius:99px;
  animation:answerGuide 1.6s ease-in-out infinite;
}


.question-block.show .question-title{
  animation:titleImpact .72s cubic-bezier(.16,.94,.25,1.20) .12s both;
}
@keyframes titleImpact{
  0%{transform:translateY(26px) scale(.90);opacity:.15;filter:blur(6px)}
  68%{transform:translateY(-6px) scale(1.04);opacity:1;filter:blur(0)}
  100%{transform:none;opacity:1;filter:none}
}


.comparison.show{
  animation:comparisonBurst .72s cubic-bezier(.18,.88,.24,1.08) both;
}
@keyframes comparisonBurst{
  0%{opacity:0;transform:translateY(34px) scale(.94);filter:blur(5px)}
  68%{opacity:1;transform:translateY(-5px) scale(1.015);filter:blur(0)}
  100%{opacity:1;transform:none;filter:none}
}
.comparison.show .compare-head .ashita{
  animation:ashitaColumnPop .64s cubic-bezier(.18,.92,.28,1.16) .22s both;
}
@keyframes ashitaColumnPop{
  0%{transform:translateY(-8px) scale(.94)}
  70%{transform:translateY(-21px) scale(1.095)}
  100%{transform:translateY(-18px) scale(1.075)}
}

/* 5. The original comparison table transforms into the Ashita no Bus introduction */
.comparison-transition{position:relative;height:188svh;margin-top:22px}
.comparison-transition .comparison{position:sticky;top:3svh;margin-top:0;padding-top:18px;min-height:94svh;will-change:transform}
.compare-head > div,.compare-grid .cell,.recommend-tag,.column-glow{will-change:opacity,transform,filter}
.ashita-focus-card{position:absolute;z-index:20;left:var(--focus-left,64px);top:var(--focus-top,34px);width:var(--focus-width,100px);height:var(--focus-height,610px);border:4px solid var(--blue);border-radius:18px;background:linear-gradient(180deg,#f4faff 0%,#e7f5ff 100%);box-shadow:0 20px 46px rgba(22,95,227,.24),8px 9px 0 var(--yellow);opacity:0;overflow:hidden;pointer-events:none;transform-origin:center top;will-change:left,top,width,height,opacity,transform,border-radius}
.ashita-focus-card .focus-column-preview{position:relative;z-index:1;height:100%;display:flex;flex-direction:column;opacity:1;will-change:opacity}
.focus-preview-head{min-height:96px;display:grid;place-items:center;padding:14px 7px;background:linear-gradient(180deg,#2374ee 0%,#1559d6 100%);color:#fff;text-align:center;font-size:13px;line-height:1.35;font-weight:950}
.focus-preview-row{flex:1;min-height:110px;display:grid;place-items:center;padding:12px 7px;border-top:1px solid #dce8f1;color:var(--deep);text-align:center;font-size:12px;line-height:1.45;font-weight:950}
.focus-preview-row strong{display:block;color:var(--pink);font-size:15px}
.focus-preview-row .mark{font-size:25px}
.focus-about{position:absolute;z-index:3;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:26px 22px;text-align:center;opacity:0;transform:translateY(14px) scale(.96);will-change:opacity,transform;background:linear-gradient(180deg,#f8fcff 0%,#eef8ff 100%)}
.focus-about .about-logo{width:150px;margin:0 auto 14px}
.focus-about .about-eyebrow{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  margin:0 0 12px;
  padding:6px 12px;
  border-radius:999px;
  background:var(--yellow);
  color:var(--deep);
  font-size:12px;
  line-height:1;
  font-weight:900;
  letter-spacing:.08em;
  box-shadow:3px 4px 0 rgba(255,111,158,.18);
}

.focus-about h3{
  margin:0;
  width:100%;
  color:var(--deep);
  font-size:clamp(24px,6.2vw,32px);
  line-height:1.15;
  letter-spacing:-.045em;
  font-weight:950;
  text-align:center;
  white-space:nowrap;
  word-break:keep-all;
  overflow-wrap:normal;
}
.focus-about .about-main{margin:15px 0 0;color:#163a6f;font-size:15px;line-height:1.75;font-weight:850}
.focus-about .about-next{position:relative;margin:14px 0 0;padding:12px 14px 24px;border:0;border-radius:19px;background:rgba(255,255,255,.72);color:var(--blue);font-size:13px;line-height:1.55;font-weight:900;box-shadow:0 9px 22px rgba(22,95,227,.10)}
.focus-about .about-next:after{content:"⌄";position:absolute;left:50%;bottom:4px;transform:translateX(-50%) scale(1.02);font-size:24px;line-height:1;animation:nextCue 1.55s ease-in-out infinite}
@keyframes nextCue{0%,100%{transform:translateX(-50%) translateY(0);opacity:.5}50%{transform:translateX(-50%) translateY(5px);opacity:1}}
.section-kicker{margin:0 0 12px;color:var(--blue);font-size:12px;font-weight:900;letter-spacing:.1em}
.section-title{margin:0;font-size:clamp(34px,9.5vw,45px);line-height:1.2;letter-spacing:-.04em;font-weight:950;color:var(--deep)}


.ashita-focus-card.reading-hold{
  background:#f5fbff;
  box-shadow:0 24px 56px rgba(22,95,227,.22),8px 9px 0 var(--yellow);
}

/* 6. Four reasons: vertical scroll cards */
.merit-section{
  position:relative;
  z-index:24;
  min-height:auto;
  margin-top:0;
  padding:4px 16px 84px;
  background:linear-gradient(180deg,#f5fbff 0%,#fff8f2 15%,#f9fcff 42%,#eaf8ff 100%);
}
.merit-section{scroll-margin-top:0}

.merit-section:before{
  content:"";
  position:absolute;
  z-index:-1;
  left:50%;
  top:28px;
  width:78%;
  aspect-ratio:1;
  transform:translateX(-50%) scale(.45);
  border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,.98) 0 18%,rgba(176,228,255,.62) 46%,rgba(176,228,255,0) 74%);
  opacity:0;
  filter:blur(8px);
  pointer-events:none;
  transition:opacity .55s ease,transform .8s cubic-bezier(.16,.92,.24,1.12);
}
.merit-section:has(.merit-heading-wrap.show):before{
  opacity:1;
  transform:translateX(-50%) scale(1.25);
}


.merit-sticky-stage{
  position:relative;
  min-height:auto;
  padding:0;
  overflow:visible;
}
.merit-list{
  display:flex;
  flex-direction:column;
  gap:13px;
  margin-top:8px;
  height:auto;
  position:relative;
}




.merit-section .merit-heading-wrap{
  opacity:0;
  transform:translateY(170px) scale(.48);
  filter:blur(14px);
  transform-origin:center center;
  will-change:opacity,transform,filter;
}
.merit-section .merit-heading-wrap.show{
  animation:reasonsPopOut .86s cubic-bezier(.16,.92,.24,1.18) both;
}
@keyframes reasonsPopOut{
  0%{
    opacity:0;
    transform:translateY(170px) scale(.48);
    filter:blur(14px);
  }
  58%{
    opacity:1;
    transform:translateY(-14px) scale(1.11);
    filter:blur(0);
  }
  78%{
    transform:translateY(5px) scale(.97);
  }
  100%{
    opacity:1;
    transform:none;
    filter:none;
  }
}
@keyframes meritBurst{from{opacity:0;transform:scale(.94) translateY(12px)}to{opacity:1;transform:none}}
.merit-heading-wrap{
  position:relative;
  min-height:150px;
  margin:0 -4px 14px;
  display:flex;
  align-items:center;
  justify-content:center;
  overflow:visible;
}
.merit-character{
  position:absolute;
  z-index:1;
  bottom:4px;
  object-fit:contain;
  filter:drop-shadow(0 10px 14px rgba(24,54,102,.14));
  pointer-events:none;
}
.merit-character.rabbit{left:-7px;width:82px;animation:characterFloat 2.9s ease-in-out infinite}
.merit-character.woman{right:-8px;width:86px;animation:characterFloat 3.2s ease-in-out infinite .28s}
@keyframes characterFloat{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-6px) rotate(1.5deg)}}
.merit-spark{position:absolute;z-index:0;width:62px;height:34px;opacity:.82;pointer-events:none}
.merit-spark:before,.merit-spark:after{content:"";position:absolute;transform:rotate(45deg);border-radius:2px}
.merit-spark:before{width:10px;height:10px;background:#ffd45d;box-shadow:26px 9px 0 -2px #75d4f3,48px -4px 0 -3px #ff8fb4}
.merit-spark:after{left:7px;top:22px;width:48px;height:10px;border-top:2px dotted rgba(81,157,222,.52);background:transparent;transform:rotate(-8deg)}
.merit-spark.left{left:9px;top:12px;transform:rotate(-8deg)}
.merit-spark.right{right:7px;top:11px;transform:scaleX(-1) rotate(-8deg)}
.merit-heading{
  position:relative;
  z-index:2;
  width:72%;
  margin:0;
  padding:0 3px;
  overflow:visible;
  text-align:center;
  letter-spacing:-.04em;
}
.merit-heading .reason-title{
  display:inline-block;
  padding:8px 15px 9px;
  border-radius:999px;
  background:linear-gradient(90deg,#ff7fa6,#ff9a82);
  color:#fff;
  font-size:clamp(18px,4.8vw,24px);
  line-height:1.16;
  font-weight:950;
  white-space:nowrap;
  box-shadow:0 8px 18px rgba(255,111,158,.22);
  text-shadow:0 2px 0 rgba(173,42,82,.16);
}
.merit-heading .reason-title .line{display:block}
.merit-heading .merit-count{
  display:flex;
  align-items:baseline;
  justify-content:center;
  gap:.015em;
  margin-top:15px;
  font-size:clamp(42px,10.7vw,55px);
  line-height:1;
  font-weight:1000;
  letter-spacing:-.065em;
  filter:drop-shadow(0 5px 11px rgba(23,74,150,.14));
}
.merit-heading .count-number{
  display:inline-block;
  font-size:1.18em;
  color:#ff8a69;
  background:linear-gradient(145deg,#ff756f 0%,#ffb33e 92%);
  -webkit-background-clip:text;
  background-clip:text;
  -webkit-text-fill-color:transparent;
  text-shadow:none;
  filter:drop-shadow(3px 3px 0 #fff) drop-shadow(5px 5px 0 rgba(255,211,143,.55));
}
.merit-heading .count-unit{color:#17366e;text-shadow:3px 3px 0 #fff}
.merit-heading .count-reason{color:#2a86e8;text-shadow:3px 3px 0 #fff,5px 5px 0 rgba(145,215,250,.4)}

.merit-list{
  display:flex;
  flex-direction:column;
  gap:18px;
  margin-top:8px;
}
.merit-card{
  --card-accent:#ffb93e;
  position:relative;
  display:grid;
  grid-template-columns:60px 1fr;
  gap:13px;
  align-items:start;
  min-height:auto;
  padding:17px 15px 18px;
  border:2px solid rgba(255,255,255,.94);
  border-radius:27px;
  overflow:hidden;
  background:linear-gradient(145deg,#fffdf7 0%,#fff1c6 100%);
  box-shadow:0 18px 42px rgba(34,75,128,.15),inset 0 0 0 1px rgba(28,69,123,.04);
  opacity:0;
  transform:translateY(70px) scale(.92);
  pointer-events:auto;
  will-change:transform,opacity,filter;
  filter:blur(7px);
  transition:none;
}
.merit-card:before{
  content:"";
  position:absolute;
  inset:0;
  background:
    radial-gradient(circle at 8% 8%,rgba(255,255,255,.98),transparent 34%),
    linear-gradient(90deg,var(--card-accent) 0 7px,transparent 7px);
  pointer-events:none;
}

.merit-heading-wrap.show + .merit-list .merit-card{
  animation:meritCardPop .72s cubic-bezier(.16,.92,.24,1.12) both;
}
.merit-heading-wrap.show + .merit-list .merit-card:nth-child(1){animation-delay:.16s}
.merit-heading-wrap.show + .merit-list .merit-card:nth-child(2){animation-delay:.30s}
.merit-heading-wrap.show + .merit-list .merit-card:nth-child(3){animation-delay:.44s}
.merit-heading-wrap.show + .merit-list .merit-card:nth-child(4){animation-delay:.58s}

@keyframes meritCardPop{
  0%{opacity:0;transform:translateY(70px) scale(.92);filter:blur(7px)}
  68%{opacity:1;transform:translateY(-5px) scale(1.02);filter:blur(0)}
  100%{opacity:1;transform:none;filter:none}
}
.merit-card:hover{
  box-shadow:0 20px 42px rgba(34,75,128,.16),inset 0 0 0 1px rgba(28,69,123,.04);
}
.merit-card.price{--card-accent:#ffbd42;background:linear-gradient(145deg,#fffdf7 0%,#ffefba 100%)}
.merit-card.safe{--card-accent:#52cfa6;background:linear-gradient(145deg,#f9fffc 0%,#d5f4e7 100%)}
.merit-card.seat{--card-accent:#57bdf0;background:linear-gradient(145deg,#f8fdff 0%,#d7efff 100%)}
.merit-card.point{--card-accent:#ea82b6;background:linear-gradient(145deg,#fff9fc 0%,#f8dcea 100%)}

.merit-card-icon{
  position:relative;
  z-index:1;
  display:grid;
  place-items:center;
  width:66px;
  height:66px;
  border-radius:21px;
  background:rgba(255,255,255,.84);
  box-shadow:0 8px 18px rgba(23,58,108,.10);
  transform:rotate(-2deg);
}
.merit-card-icon svg{width:40px;height:40px}
.merit-card-icon .cute-base{fill:#fff;opacity:.98}
.merit-card-icon .cute-main{fill:#17366e}
.merit-card-icon .cute-accent{fill:var(--card-accent)}
.merit-card-icon .cute-line{fill:none;stroke:#17366e;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.merit-card-icon .cute-white{fill:none;stroke:#fff;stroke-width:2.7;stroke-linecap:round;stroke-linejoin:round}

.merit-card-body{position:relative;z-index:1;min-width:0}
.merit-card h3{
  margin:2px 0 0;
  color:var(--deep);
  font-size:clamp(21px,5.8vw,27px);
  line-height:1.22;
  letter-spacing:-.04em;
  font-weight:950;
}
.merit-card p{
  margin:13px 0 0;
  color:#29486f;
  font-size:14px;
  line-height:1.85;
  font-weight:750;
}
.merit-card p strong{
  color:var(--blue);
  font-weight:950;
}
.merit-card.point p strong{color:#cf4f8c}



.compare-head > div,
.compare-grid .cell{
  word-break:keep-all;
  overflow-wrap:normal;
}
.compare-grid .cell > span,
.compare-grid .cell strong{
  white-space:normal;
}

/* Phone-specific layout tuning */
@media (max-width:430px){
  .hero-card{top:30%;width:86%;padding:16px 17px 17px}
  .hero-card h1{font-size:clamp(26px,6.7vw,32px)}
  .hero-card p{margin-top:10px;font-size:12px;line-height:1.55}
  .hero-hook{top:68dvh;width:82%;padding:10px 13px 7px}
  .hero-hook strong{font-size:14px;line-height:1.4}
  .hero-hook .hook-label{font-size:9px;margin-bottom:5px}
  .hero-hook .chevron{font-size:24px;margin-top:3px}

  .hero-card{top:33%;width:86%;padding:18px 18px 20px}
  .hero-logo{width:132px;margin-bottom:12px}
  .hero-official{margin-bottom:10px;font-size:10px}
  .hero-hook{bottom:2dvh}
  .question-title .line-1,.question-title .line-2{font-size:clamp(27px,7.4vw,34px)}
  .question-title .line-3{font-size:clamp(22px,5.9vw,28px)}
  .compare-section{padding-left:14px;padding-right:14px}
  .compare-head{grid-template-columns:56px 1.14fr 1fr 1fr}
  .compare-grid{grid-template-columns:56px 1.14fr 1fr 1fr}
  .column-glow{left:56px;width:calc((100% - 56px)*.363)}
  .focus-about{justify-content:center;padding:22px 18px}
  .merit-heading-wrap{margin-bottom:8px}
  .merit-heading .reason-title{font-size:16px}
  .merit-heading .merit-count{font-size:40px;margin-top:10px}
  .merit-character.rabbit{width:68px}
  .merit-character.woman{width:72px}
  .cta-section .section-title{font-size:clamp(22px,6vw,29px)}
}
@media (max-height:760px){
  .hero-card{top:31%;padding-top:15px;padding-bottom:16px}
  .hero-card h1{font-size:27px}
  .hero-card p{font-size:12px;line-height:1.55}
  .hero-hook{padding:10px 14px 7px}
  .hero-hook strong{font-size:14px}
  .hero-hook .chevron{font-size:26px}
  .focus-about .about-logo{width:128px;margin-bottom:10px}
  .focus-about .about-main{font-size:13px;line-height:1.6;margin-top:11px}
  .focus-about .about-next{font-size:12px;margin-top:10px;padding:10px 12px 21px}
  .cta-city-wrap{height:205px}
}

@media(max-width:370px){
  .merit-card{
    grid-template-columns:60px 1fr;
    gap:13px;
    padding:18px 15px 20px;
  }
  .merit-card-icon{
    width:56px;
    height:56px;
    border-radius:18px;
  }
  .merit-card-icon svg{width:40px;height:40px}
  .merit-card h3{font-size:23px}
  .merit-card p{font-size:13px}
}

/* 7. CTA */
.cta-section{
  min-height:auto;
  padding:42px 20px 74px;
  text-align:center;
  background:linear-gradient(180deg,#e8f8ff 0%,#fff 48%,#d7f1ff 100%);
}
.cta-city-wrap{
  position:relative;
  height:230px;
  margin:0 -24px 26px;
  overflow:hidden;
  border-radius:0;
  background:linear-gradient(180deg,#eafaff 0%,#dff6ff 100%);
}
.cta-city-bg{
  position:absolute;
  z-index:1;
  left:50%;
  top:38px;
  width:88%;
  height:auto;
  max-width:none;
  transform:translateX(-50%);
  object-fit:contain;
  object-position:center top;
}
.cta-bus{
  position:absolute;
  z-index:2;
  left:50%;
  bottom:18px;
  width:88%;
  max-width:360px;
  transform:translateX(-50%);
  filter:drop-shadow(0 12px 18px rgba(17,63,105,.20));
  animation:ctaBusFloat 2.8s ease-in-out infinite;
}
@keyframes ctaBusFloat{
  0%,100%{transform:translateX(-50%) translateY(0)}
  50%{transform:translateX(-50%) translateY(-4px)}
}
.cta-message{
  margin:0 0 20px;
  padding:20px 16px 18px;
  border:1px solid rgba(255,255,255,.9);
  border-radius:25px;
  background:rgba(255,255,255,.94);
  box-shadow:0 16px 36px rgba(22,95,227,.12);
  backdrop-filter:blur(6px);
  -webkit-backdrop-filter:blur(6px);
}
.cta-section .section-title{
  margin:0;
  color:var(--deep);
  font-size:clamp(22px,6vw,31px);
  line-height:1.3;
  letter-spacing:-.045em;
  font-weight:950;
}
.cta-section .section-title .cta-title-line{
  display:block;
  white-space:nowrap;
  word-break:keep-all;
}
.cta-section .section-title .accent{
  margin-top:3px;
  color:var(--blue);
  font-size:.88em;
  letter-spacing:-.055em;
}
.cta-copy{
  margin:17px 0 0;
  color:#4b627f;
  font-size:15px;
  line-height:1.8;
  font-weight:800;
}
.primary-cta-wrap{
  margin-top:2px;
}
.primary-microcopy{
  margin:0 0 10px;
  color:var(--deep);
  font-size:12px;
  line-height:1.3;
  font-weight:950;
  letter-spacing:.015em;
}
.cta-button{
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  width:100%;
  min-height:60px;
  border-radius:999px;
  color:#fff;
  font-size:17px;
  line-height:1.35;
  font-weight:950;
  transition:transform .2s ease,box-shadow .2s ease,background .2s ease;
}
.cta-button:hover{
  transform:translateY(-2px);
}
.cta-button:active{
  transform:translateY(0) scale(.985);
}
.cta-button.primary{
  background:linear-gradient(180deg,#2879ee 0%,#165fe3 100%);
  box-shadow:0 15px 30px rgba(22,95,227,.28);
}
.cta-button.primary span{
  font-size:13px;
  font-weight:850;
  opacity:.9;
}
.cta-button.primary strong{
  display:block;
  font-size:18px;
}
.line-cta-wrap{
  margin-top:16px;
}
.line-microcopy{
  margin:0 0 10px;
  white-space:nowrap;
  color:#263a58;
  font-size:13px;
  line-height:1;
  font-weight:950;
  letter-spacing:.04em;
}
.cta-button.line{
  min-height:58px;
  background:#06C755;
  box-shadow:0 14px 28px rgba(6,199,85,.25);
}
.cta-button.line:hover{
  background:#05B84E;
}
@media(max-width:370px){
  :root{--rail:25px}
  .compare-section{padding-left:14px;padding-right:14px}
  .compare-head{grid-template-columns:57px 1.14fr 1fr 1fr}
  .compare-grid{grid-template-columns:57px 1.14fr 1fr 1fr}
  .column-glow{left:57px;width:calc((100% - 57px)*.363)}
  .cell{font-size:10px;padding:10px 4px}
  .merit-tile h3{font-size:19px}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*:before,*:after{animation:none!important;transition:none!important}
  .reveal{opacity:1!important;transform:none!important}
  .merit-card{opacity:1!important;transform:none!important;filter:none!important}
}
</style>

<script>
(function syncStreamlitFrameToViewport(){
  const getVisibleHeight=()=>{
    try{
      const parentHeight=window.parent.innerHeight;
      if(parentHeight && parentHeight>300) return parentHeight;
    }catch(error){}
    if(window.visualViewport && window.visualViewport.height>300){
      return window.visualViewport.height;
    }
    return Math.min(window.screen?.availHeight||760,760);
  };

  const sendHeight=()=>{
    const height=Math.max(560,Math.round(getVisibleHeight()));
    window.parent.postMessage({
      isStreamlitMessage:true,
      type:"streamlit:setFrameHeight",
      height
    },"*");
  };

  sendHeight();
  addEventListener("load",sendHeight);
  addEventListener("resize",sendHeight);
  addEventListener("orientationchange",()=>setTimeout(sendHeight,120));
  window.visualViewport?.addEventListener("resize",sendHeight);
})();
</script>

</head>
<body>
<div class="lp">
  <section class="section hero" id="top">
    <div class="hero-stage">
      <div class="hero-photo"></div>
      <div class="hero-light"></div>
      <div class="hero-whiteout"></div>
      <div class="hero-world" aria-hidden="true"><div class="hero-world-road"></div><img class="hero-world-bus" src="__BUS__" alt=""><div class="hero-world-bubble">予約、<br>まだ待って！</div></div>
      <div class="hero-card reveal">
        <span class="hero-official">ナイトライナー車内限定</span>
        <img class="hero-logo" src="__LOGO__" alt="あしたのバス">
        <h1><span>ご乗車</span><span class="thanks">ありがとうございます。</span></h1>
        <p>目的地まで、<br>どうぞごゆっくりお過ごしください。</p>
      </div>
      <a class="hero-hook" href="#portal">
        <span class="hook-label">車内限定のご案内</span>
        <strong>次回もナイトライナーを<br>ご利用予定のあなたへ</strong>
        <span class="chevron">⌄</span>
      </a>
    </div>
  </section>

  <section class="section portal" id="portal">
    <div class="portal-glow"></div>
  </section>

  <div class="pop-world" id="pop-world">
    <aside class="rail left"><div class="rail-stack">__RAILS__</div></aside>
    <aside class="rail right"><div class="rail-stack">__RAILS__</div></aside>
    <main class="pop-content">
      <section class="compare-section" id="compare">
        <div class="question-block reveal">
          <h2 class="question-title">
<span class="line line-1">ナイトライナー、</span>
<span class="line line-2">どこで予約しても</span>
<span class="line line-3 accent">同じだと思っていませんか？</span>
</h2>
          <div class="question-answer" aria-label="予約先によって価格やサービスに違いがあります。">
            <img class="answer-cat" src="__CAT__" alt="猫のキャラクター">
            <div class="answer-bubble">
              <span class="answer-kicker">実は…</span>
              <p><span>予約先によって</span><span>価格やサービスに違いがあります。</span></p>
            </div>
          </div>
        </div>

        <div class="comparison-transition">
          <div class="comparison reveal">
          <div class="recommend-tag">おすすめ</div>
          <div class="compare-head">
            <div class="blank"></div>
            <div class="ashita">あしたのバス</div>
            <div>ナイトライナー<br>（直販）</div>
            <div>他社予約<br>サイト</div>
          </div>
          <div class="compare-grid">
            <div class="cell label"><span class="label-wrap"><span class="label-icon price">¥</span>料金</span></div>
            <div class="cell ashita first"><span><strong>直販より<br>最安値</strong><span class="mark good">◎</span></span></div>
            <div class="cell">直販価格<span class="mark mid">○</span></div>
            <div class="cell">サイトにより異なる<span class="mark mid">△</span></div>


            <div class="cell label"><span class="label-wrap"><span class="label-icon seat">▣</span>座席指定</span></div>
            <div class="cell ashita"><span><strong>指定可能</strong><span class="mark good">◎</span></span></div>
            <div class="cell">指定可能<span class="mark good">◎</span></div>
            <div class="cell">指定不可<span class="mark bad">×</span></div>

            <div class="cell label"><span class="label-wrap"><span class="label-icon point">P</span>ポイント</span></div>
            <div class="cell ashita last"><span><strong>貯まる！<br>使える！</strong><span class="mark good">◎</span></span></div>
            <div class="cell">なし<span class="mark bad">×</span></div>
            <div class="cell">サイトにより異なる<span class="mark mid">△</span></div>
            <div class="column-glow"></div>
          </div>
          <div class="ashita-focus-card" aria-hidden="true">
            <div class="focus-column-preview">
              <div class="focus-preview-head">あしたのバス</div>
              <div class="focus-preview-row"><span><strong>直販より<br>最安値</strong><span class="mark good">◎</span></span></div>
              <div class="focus-preview-row"><span><strong>指定可能</strong><span class="mark good">◎</span></span></div>
              <div class="focus-preview-row"><span><strong>貯まる！<br>使える！</strong><span class="mark good">◎</span></span></div>
            </div>
            <div class="focus-about">
              <img class="about-logo" src="__LOGO__" alt="あしたのバス">
              <span class="about-eyebrow">＼ そもそも ／</span><h3>あしたのバスって？</h3>
              <p class="about-main">東京富士交通が運営する、<br>全国の高速・夜行バスを予約できる<br>予約サイトです。</p>
              <p class="about-next">さらにスクロールすると、<br>選ばれる4つの理由が登場！</p>
            </div>
          </div>
        </div>
        </div>
      </section>

      <section class="merit-section" id="merits">
        <div class="merit-sticky-stage">
        <div class="merit-heading-wrap reveal">
          <span class="merit-spark left" aria-hidden="true"></span>
          <span class="merit-spark right" aria-hidden="true"></span>
          <img class="merit-character rabbit" src="__USAGI__" alt="うさぎキャラクター">
          <h2 class="merit-heading">
            <span class="reason-title"><span class="line">あしたのバスが選ばれる</span></span>
            <span class="merit-count">
              <span class="count-number">4</span>
              <span class="count-unit">つの</span>
              <span class="count-reason">理由</span>
            </span>
          </h2>
          <img class="merit-character woman" src="__WOMEN__" alt="女性キャラクター">
        </div>

        <div class="merit-list">
          <article class="merit-card price reveal-card">
            <div class="merit-card-icon" aria-hidden="true">
              <svg viewBox="0 0 48 48">
                <rect class="cute-accent" x="8" y="17" width="32" height="24" rx="7"/>
                <path class="cute-main" d="M14 13h20a6 6 0 0 1 6 6v5H8v-5a6 6 0 0 1 6-6Z"/>
                <circle class="cute-base" cx="24" cy="13" r="6"/>
                <path class="cute-line" d="M24 8v10M20.5 11.5h7M20.5 15h7"/>
                <circle class="cute-base" cx="34" cy="30" r="3"/>
              </svg>
            </div>
            <div class="merit-card-body">
              <h3>直販より最安値</h3>
              <p>ナイトライナーの運行会社が運営する予約サイトだからこそ、外部コストを抑え、<strong>直販よりお得な価格</strong>でご予約いただけます。</p>
            </div>
          </article>

          <article class="merit-card safe reveal-card">
            <div class="merit-card-icon" aria-hidden="true">
              <svg viewBox="0 0 48 48">
                <path class="cute-accent" d="M24 4.5c5.2 4 10.4 6.4 16.5 7.4v10.2c0 10.8-6.7 18-16.5 21.5C14.2 40.1 7.5 32.9 7.5 22.1V11.9C13.6 10.9 18.8 8.5 24 4.5Z"/>
                <path class="cute-base" d="M24 31.5c-6.7-4.2-10-7.4-10-11.2 0-2.9 2-5 4.8-5 2 0 3.8 1.1 5.2 3 1.4-1.9 3.2-3 5.2-3 2.8 0 4.8 2.1 4.8 5 0 3.8-3.3 7-10 11.2Z"/>
              </svg>
            </div>
            <div class="merit-card-body">
              <h3>安全性を重視</h3>
              <p>安心してご利用いただけるよう、<strong>安全への取り組みを重視する運行会社</strong>の便のみを掲載しています。</p>
            </div>
          </article>

          <article class="merit-card seat reveal-card">
            <div class="merit-card-icon" aria-hidden="true">
              <svg viewBox="0 0 48 48">
                <rect class="cute-accent" x="8" y="6" width="13" height="24" rx="6"/>
                <path class="cute-main" d="M10 25h17c6 0 10 4 10 10v5H17c-5 0-9-4-9-9v-6Z"/>
                <path class="cute-line" d="M17 40v4M37 40v4"/>
                <path class="cute-base" d="M13 11h4v10h-4z"/>
              </svg>
            </div>
            <div class="merit-card-body">
              <h3>好きな席を選べる</h3>
              <p>座席指定に対応している便では、予約時に<strong>ご希望の座席</strong>をお選びいただけます。</p>
            </div>
          </article>

          <article class="merit-card point reveal-card">
            <div class="merit-card-icon" aria-hidden="true">
              <svg viewBox="0 0 48 48">
                <circle class="cute-accent" cx="18" cy="19" r="13"/>
                <circle class="cute-base" cx="18" cy="19" r="8"/>
                <circle class="cute-main" cx="31" cy="30" r="12"/>
                <path class="cute-white" d="M28 36V24h4.4a4 4 0 0 1 0 8H28"/>
                <path class="cute-line" d="M14 16h8M18 12v14"/>
              </svg>
            </div>
            <div class="merit-card-body">
              <h3>ポイントが貯まる・使える</h3>
              <p>ご乗車やキャンペーンでポイントが貯まり、<strong>1ポイント＝1円</strong>としてチケット購入にご利用いただけます。</p>
            </div>
          </article>
        </div>
        </div>
      </section>

      <section class="cta-section" id="cta">
  <div class="cta-city-wrap reveal">
    <img class="cta-city-bg" src="__CITY__" alt="">
    <img class="cta-bus" src="__BUS__" alt="あしたのバス">
  </div>

  <div class="cta-message reveal">
    <h2 class="section-title">
      <span class="cta-title-line">次のナイトライナーも、</span>
      <span class="cta-title-line accent">あなたに合った予約で<br>もっと快適に。</span>
    </h2>
    <p class="cta-copy">
      全国の高速・夜行バスの<br>
      空席・料金を今すぐチェック。
    </p>
  </div>

  <div class="primary-cta-wrap reveal">
    <p class="primary-microcopy">＼ 直販より最安＆座席指定OK！ ／</p>
    <a class="cta-button primary"
     href="__SITE__"
     target="_blank"
     rel="noopener noreferrer">
     <span>あしたのバス</span>
     <strong>予約サイトはこちら&nbsp; ＞</strong>
    </a>
  </div>

  <div class="line-cta-wrap reveal">
    <p class="line-microcopy">＼ お得な情報を配信中！ ／</p>
    <a class="cta-button line"
       href="https://page.line.me/560isyhl"
       target="_blank"
       rel="noopener noreferrer">
       公式LINEはこちら&nbsp; ＞
    </a>
  </div>
</section>
    </main>
  </div>
</div>

<script>
const revealItems=document.querySelectorAll('.reveal');
const revealObserver=new IntersectionObserver((entries)=>{
  entries.forEach((entry)=>{
    if(entry.isIntersecting){entry.target.classList.add('show');revealObserver.unobserve(entry.target);}
  });
},{threshold:.14,rootMargin:'0px 0px -7% 0px'});
revealItems.forEach((item)=>revealObserver.observe(item));

const hero=document.querySelector('.hero');
const hook=document.querySelector('.hero-hook');
const photo=document.querySelector('.hero-photo');
const light=document.querySelector('.hero-light');
const whiteout=document.querySelector('.hero-whiteout');
const heroWorld=document.querySelector('.hero-world');
const heroWorldBus=document.querySelector('.hero-world-bus');
const heroWorldBubble=document.querySelector('.hero-world-bubble');
const heroCard=document.querySelector('.hero-card');
const portal=document.querySelector('.portal');
const rails=document.querySelectorAll('.rail');
const comparisonTransition=document.querySelector('.comparison-transition');
const comparisonBox=document.querySelector('.comparison');
const focusCard=document.querySelector('.ashita-focus-card');
const focusPreview=document.querySelector('.focus-column-preview');
const focusAbout=document.querySelector('.focus-about');

const comparisonSideCells=document.querySelectorAll('.compare-grid .cell:not(.ashita)');
const comparisonSideHeads=document.querySelectorAll('.compare-head > div:not(.ashita)');
const comparisonAshitaCells=document.querySelectorAll('.compare-grid .cell.ashita');
const comparisonAshitaHead=document.querySelector('.compare-head .ashita');
const recommendation=document.querySelector('.recommend-tag');
const columnGlow=document.querySelector('.column-glow');
const clamp=(value,min=0,max=1)=>Math.max(min,Math.min(max,value));
const updateScroll=()=>{
  const rect=hero.getBoundingClientRect();
  const travel=Math.max(1,hero.offsetHeight-innerHeight);
  const p=clamp((-rect.top)/travel);

  // The camera advances toward the bright end of the aisle.
  const zoom=1.02+(p*1.95);
  const lift=p*9;
  photo.style.transform=`scale(${zoom}) translateY(${lift}%)`;
  photo.style.filter=`brightness(${1+(p*.5)}) saturate(${1-(p*.24)}) blur(${p*1.2}px)`;

  // The central light expands until the whole screen becomes white.
  light.style.opacity=String(.38+(p*.62));
  light.style.transform=`translate(-50%,-50%) scale(${1+(p*4.2)})`;
  const flashIn=clamp((p-.46)/.20);
  const flashOut=clamp((p-.68)/.16);
  whiteout.style.opacity=String(flashIn*(1-flashOut));

  // The light opens directly into the Ashita no Bus world.
  const worldIn=clamp((p-.60)/.18);
  heroWorld.style.opacity=String(worldIn);
  heroWorld.style.setProperty('--world-progress',String(worldIn));
  const worldGlow=heroWorld.querySelector(':scope:before');
  const busIn=clamp((p-.64)/.24);
  const busX=50+(busIn*2);
  const busY=27+(busIn*55);
  const busScale=.14+(busIn*1.02);
  heroWorldBus.style.opacity=String(busIn);
  heroWorldBus.style.left=`${busX}%`;
  heroWorldBus.style.top=`${busY}%`;
  heroWorldBus.style.transform=`translate(-50%,-50%) scale(${busScale}) rotate(${(1-busIn)*-2}deg)`;
  heroWorldBubble.style.opacity=String(clamp((p-.84)/.10));
  heroWorldBubble.style.transform=`translate(-50%,${10*(1-clamp((p-.84)/.10))}px) scale(${.88+.12*clamp((p-.84)/.10)})`;
  heroWorld.style.setProperty('filter',`saturate(${.92+.08*worldIn})`);
  heroWorld.style.setProperty('transform',`scale(${1+.015*(1-worldIn)})`);
  heroWorld.style.setProperty('transition','none');

  // Message card leaves first; the next-use hook becomes clear, then follows it.
  const cardP=clamp(p/.42);
  heroCard.style.opacity=String(1-cardP);
  heroCard.style.transform=`translate(-50%,calc(-50% - ${cardP*48}px)) scale(${1-cardP*.06})`;
  const hookIn=clamp((p-.02)/.20);
  const hookOut=1-clamp((p-.72)/.18);
  hook.style.opacity=String((.42+hookIn*.58)*hookOut);
  hook.style.transform=`translateX(-50%) translateY(${14-(hookIn*14)-(p*8)}px) scale(${.985+(hookIn*.015)})`;

  if(portal){const portalRect=portal.getBoundingClientRect();portal.classList.toggle('active',portalRect.top<innerHeight*.72);}
  const pop=document.getElementById('pop-world').getBoundingClientRect();
  rails.forEach((rail)=>rail.classList.toggle('show',p>.67 || pop.top<innerHeight*.84));

  // The original comparison table itself becomes the Ashita no Bus introduction.
  if(comparisonTransition && comparisonBox && focusCard){
    const transitionRect=comparisonTransition.getBoundingClientRect();
    const transitionTravel=Math.max(1,comparisonTransition.offsetHeight-innerHeight);
    const cp=clamp((-transitionRect.top)/transitionTravel);
    const sidesOut=clamp((cp-.06)/.22);
    const focusIn=clamp((cp-.14)/.16);
    const focusGrow=clamp((cp-.28)/.26);
    const aboutIn=clamp((cp-.44)/.08);
    // Keep the introduction readable, then cross-fade directly into the four-reasons section.
    const focusExit=clamp((cp-.88)/.08);

    comparisonSideCells.forEach((el)=>{
      el.style.opacity=String(1-sidesOut);
      el.style.filter=`blur(${sidesOut*2}px)`;
    });
    comparisonSideHeads.forEach((el,index)=>{
      el.style.opacity=String(1-sidesOut);
      const direction=index===0?-1:1;
      el.style.transform=`translateX(${direction*36*sidesOut}px)`;
    });
    recommendation.style.opacity=String(1-clamp((cp-.18)/.18));
    columnGlow.style.opacity=String(1-clamp((cp-.24)/.16));

    const boxRect=comparisonBox.getBoundingClientRect();
    const headRect=comparisonAshitaHead.getBoundingClientRect();
    const lastRect=comparisonAshitaCells[comparisonAshitaCells.length-1].getBoundingClientRect();
    const startLeft=headRect.left-boxRect.left;
    const startTop=headRect.top-boxRect.top;
    const startWidth=headRect.width;
    const startHeight=lastRect.bottom-headRect.top;
    const targetLeft=10;
    const targetWidth=Math.max(260,comparisonBox.clientWidth-20);
    const targetHeight=Math.min(innerHeight*.78,560);
    // Center the expanded card so the screen never becomes a large empty white area.
    const targetTop=Math.max(4,(innerHeight-targetHeight)/2);
    const mix=(a,b,t)=>a+(b-a)*t;

    focusCard.style.left=`${mix(startLeft,targetLeft,focusGrow)}px`;
    focusCard.style.top=`${mix(startTop,targetTop,focusGrow)}px`;
    focusCard.style.width=`${mix(startWidth,targetWidth,focusGrow)}px`;
    focusCard.style.height=`${mix(startHeight,targetHeight,focusGrow)}px`;
    focusCard.style.borderRadius=`${mix(18,30,focusGrow)}px`;
    focusCard.style.opacity=String(focusIn*(1-focusExit));
    focusCard.style.transform=`translateY(${-10*focusExit}px) scale(${1-.015*focusExit})`;

    const originalAshitaOpacity=1-clamp((cp-.24)/.16);
    comparisonAshitaCells.forEach((el)=>el.style.opacity=String(originalAshitaOpacity));
    comparisonAshitaHead.style.opacity=String(originalAshitaOpacity);

    const previewOut=clamp((cp-.40)/.08);
    focusPreview.style.opacity=String(1-previewOut);
    const aboutOpacity=aboutIn*(1-focusExit);
    focusAbout.style.opacity=String(aboutOpacity);
    focusAbout.style.transform=`translateY(${-18*focusExit + 8*(1-aboutIn)}px) scale(${.985+.015*aboutIn-.018*focusExit})`;
    focusCard.classList.toggle('reading-hold',cp>=.54 && cp<.88);

    // As the overview moves upward, the four-reasons heading rises into the same visual position.
    if(meritHeading){
      const meritIn=clamp((cp-.74)/.22);
      const meritPop=meritIn<.72
        ? meritIn/.72
        : 1 + Math.sin((meritIn-.72)/.28*Math.PI)*.11;
      const meritScale=.62+(.38*Math.min(1,meritPop));
      const meritY=180*(1-meritIn);
      const meritRotate=12*(1-meritIn);

      meritHeading.style.opacity=String(meritIn);
      meritHeading.style.transform=`translateY(${meritY}px) scale(${meritScale}) rotateX(${meritRotate}deg)`;
      meritHeading.style.filter=`blur(${12*(1-meritIn)}px)`;

      if(meritSection){
        meritSection.style.setProperty('--merit-pop',String(meritIn));
      }
    }
  }
};
addEventListener('scroll',updateScroll,{passive:true});
updateScroll();

</script>
</body>
</html>'''

    rail_unit = f'<div class="rail-slot"><img class="rail-unit" src="{a["logo"]}" alt="あしたのバス"></div>'
    rail_stack = rail_unit * 9
    replacements = {
        "__INTERIOR__": a["interior"],
        "__RAILS__": rail_stack,
        "__DOG__": a["dog"],
        "__BUS__": a["bus"],
        "__CITY__": a["city"],
        "__LOGO__": a["logo"],
        "__WOMEN__": a["women"],
        "__USAGI__": a["usagi"],
        "__CAT__": a["cat"],
        "__SITE__": SITE_URL,
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def render() -> None:
    try:
        assets = load_assets()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.info("このPythonファイルと同じ場所に assets フォルダを置いてください。")
        st.stop()
    st.components.v1.html(build_html(assets), height=720, scrolling=True)


def main() -> None:
    st.set_page_config(
        page_title="あしたのバス｜ナイトライナー",
        page_icon="🚌",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    streamlit_shell_css()
    render()


if __name__ == "__main__":
    main()