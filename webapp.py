"""SALIM AI web dashboard with browser microphone and speech output."""
import os
import re
from flask import Flask, request, session, redirect, url_for, render_template_string, jsonify
from dotenv import load_dotenv
from ai_client import ask_gemini
from browser_actions import handle_command

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or os.urandom(32).hex()
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
PASSWORD = os.getenv("DASHBOARD_PASSWORD", "").strip()
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are SALIM AI, a helpful bilingual assistant. Understand Hausa and English. Reply in the language the user uses. Be honest when unsure.")

HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0b1220"><title>SALIM AI | Voice Dashboard</title>
<style>
:root{color-scheme:dark;--bg:#0b1220;--panel:#121e31;--panel2:#17263d;--line:#293b56;--text:#edf5ff;--muted:#a8bad0;--blue:#38bdf8;--green:#34d399}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at top,#162a45 0,#0b1220 55%);font-family:system-ui,-apple-system,Segoe UI,sans-serif;color:var(--text);min-height:100vh;padding:20px 12px}
.wrap{max-width:850px;margin:0 auto}.top{display:flex;align-items:center;gap:13px;margin:8px 0 20px}.logo{width:52px;height:52px;border-radius:17px;background:linear-gradient(135deg,#0284c7,#34d399);display:grid;place-items:center;font-size:25px;box-shadow:0 8px 30px #0284c733}.brand h1{font-size:clamp(22px,5vw,32px);margin:0;letter-spacing:.2px}.brand p{margin:3px 0;color:var(--muted);font-size:13px}.status{margin-left:auto;border:1px solid var(--line);border-radius:99px;padding:7px 10px;font-size:12px;color:var(--green);white-space:nowrap}
.panel{background:#111d2eee;border:1px solid var(--line);border-radius:22px;padding:clamp(14px,4vw,24px);box-shadow:0 18px 50px #0003}.welcome h2{margin:0 0 6px;font-size:21px}.welcome p{margin:0;color:var(--muted);line-height:1.55}.quick{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}.chip{background:var(--panel2);border:1px solid var(--line);border-radius:99px;padding:8px 12px;color:#d9eaff;font-size:13px;cursor:pointer}.chat{display:flex;flex-direction:column;gap:12px;margin:18px 0;max-height:45vh;overflow:auto}.msg{max-width:95%;padding:12px 14px;border-radius:16px;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.55}.user{align-self:flex-end;background:#075985}.assistant{align-self:flex-start;background:var(--panel2);border:1px solid var(--line)}.muted{color:var(--muted);font-size:12px}.compose{display:flex;gap:8px;align-items:stretch}.compose textarea{flex:1;min-width:0;resize:vertical;min-height:52px;max-height:150px;background:#0b1525;border:1px solid #38506e;color:var(--text);border-radius:14px;padding:14px;font:inherit;outline:none}.compose textarea:focus{border-color:var(--blue)}button{font:inherit;font-weight:650;cursor:pointer;border:0;border-radius:14px;padding:12px 15px;color:#041321;background:var(--blue)}button:disabled{opacity:.5;cursor:wait}.mic{background:var(--green);min-width:54px;font-size:20px}.mic.listening{background:#fb7185;color:#25040b;animation:pulse 1.1s infinite}.secondary{background:#24364e;color:var(--text);border:1px solid var(--line)}.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.actions button{font-size:13px;padding:9px 12px}.note{margin-top:15px;color:var(--muted);font-size:12px;line-height:1.5}.login{max-width:430px;margin:12vh auto}.login input{width:100%;padding:13px;background:#0b1525;border:1px solid var(--line);border-radius:12px;color:white;margin:10px 0}.login button{width:100%}a{color:var(--blue)}@keyframes pulse{50%{box-shadow:0 0 0 7px #fb718533}}@media(max-width:520px){body{padding:12px 9px}.status{font-size:10px}.compose{flex-wrap:wrap}.compose textarea{flex-basis:100%}.compose button{flex:1}.msg{max-width:100%}}
</style></head><body><div class="wrap">
<div class="top"><div class="logo">✦</div><div class="brand"><h1>SALIM AI</h1><p>Hausa • English • Voice Assistant</p></div><div class="status" id="status">● Ready</div></div>
{% if not logged_in %}<div class="panel login"><h2>Shiga SALIM AI</h2><p class="muted">Saka kalmar sirrin dashboard.</p><form method="post" action="/login"><input type="password" name="password" placeholder="Dashboard password" required><button type="submit">Login</button></form></div>
{% else %}<div class="panel"><div class="welcome"><h2>Sannu! Ina sauraro.</h2><p>Rubuta ko ka yi magana da Hausa ko Turanci. Taɓa microphone domin fara magana.</p></div>
<div class="quick"><button class="chip" data-prompt="SALIM, ya kake?">👋 Gaisuwa</button><button class="chip" data-prompt="Buɗe min YouTube">▶ Buɗe YouTube</button><button class="chip" data-prompt="Ka yi mini bayani a Hausa game da AI">✦ Tambayi AI</button></div>
<div class="chat" id="chat" aria-live="polite"><div class="msg assistant">Ni ne SALIM AI. Taɓa microphone ko rubuta tambayarka a ƙasa.</div></div>
<form id="chatForm"><div class="compose"><textarea id="prompt" rows="1" placeholder="Rubuta saƙonka…" aria-label="Saƙo"></textarea><button class="mic" id="mic" type="button" title="Fara magana" aria-label="Microphone">🎙️</button><button id="send" type="submit">Aika ➤</button></div></form>
<div class="actions"><button type="button" class="secondary" id="speakToggle">🔊 Amsar murya: ON</button><button type="button" class="secondary" id="clear">Share hira</button><form method="post" action="/logout" style="margin-left:auto"><button class="secondary" type="submit">Fita</button></form></div>
<p class="note" id="voiceNote">Microphone yana amfani da fasalin browser. Ka amince da izinin microphone idan an tambaye ka. Gane magana ya danganta da browser da harshen da yake goyon baya.</p>
{% endif %}</div></div>
<script>
const chat=document.getElementById('chat');
if(chat){
 const promptBox=document.getElementById('prompt'),form=document.getElementById('chatForm'),send=document.getElementById('send'),mic=document.getElementById('mic'),status=document.getElementById('status'),speakToggle=document.getElementById('speakToggle');
 let speakOn=true,recognition=null,listening=false;
 function addMsg(text,who){const el=document.createElement('div');el.className='msg '+who;el.textContent=text;chat.appendChild(el);chat.scrollTop=chat.scrollHeight;return el}
 function setStatus(s){status.textContent='● '+s}
 function speak(text){if(!speakOn||!('speechSynthesis'in window))return;window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.lang=/[ƙɗɓƴ]/i.test(text)||/\b(ina|menene|yaya|na gode|bude|buɗe)\b/i.test(text)?'ha-NG':'en-NG';u.rate=1;window.speechSynthesis.speak(u)}
 async function sendMessage(text){text=(text||'').trim();if(!text)return;addMsg(text,'user');promptBox.value='';send.disabled=true;setStatus('Ina tunani…');const waiting=addMsg('SALIM AI yana tunani…','assistant');try{const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});const data=await res.json();waiting.textContent=data.answer||data.error||'Ba a samu amsa ba.';speak(waiting.textContent);setStatus('Ready')}catch(e){waiting.textContent='An samu matsalar haɗi. Duba intanet sannan ka sake gwadawa.';setStatus('Connection error')}finally{send.disabled=false;promptBox.focus()}}
 form.addEventListener('submit',e=>{e.preventDefault();sendMessage(promptBox.value)});
 document.querySelectorAll('[data-prompt]').forEach(b=>b.addEventListener('click',()=>sendMessage(b.dataset.prompt)));
 document.getElementById('clear').addEventListener('click',()=>{chat.innerHTML='';addMsg('An share hirar. Me zan taimaka maka?','assistant');if('speechSynthesis'in window)speechSynthesis.cancel()});
 speakToggle.addEventListener('click',()=>{speakOn=!speakOn;speakToggle.textContent='🔊 Amsar murya: '+(speakOn?'ON':'OFF');if(!speakOn&&'speechSynthesis'in window)speechSynthesis.cancel()});
 const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(SpeechRecognition){recognition=new SpeechRecognition();recognition.continuous=false;recognition.interimResults=true;recognition.lang='ha-NG';recognition.onstart=()=>{listening=true;mic.classList.add('listening');mic.textContent='⏹️';setStatus('Ina sauraro…')};recognition.onresult=e=>{let interim='',finalText='';for(let i=e.resultIndex;i<e.results.length;i++){if(e.results[i].isFinal)finalText+=e.results[i][0].transcript;else interim+=e.results[i][0].transcript}promptBox.value=finalText||interim;if(finalText){recognition.finalTranscript=finalText}};recognition.onerror=e=>{setStatus('Microphone: '+e.error);if(e.error==='not-allowed')document.getElementById('voiceNote').textContent='An hana microphone. Ka buɗe site settings na browser ka ba shi izinin Microphone.'};recognition.onend=()=>{listening=false;mic.classList.remove('listening');mic.textContent='🎙️';setStatus('Ready');const spoken=recognition.finalTranscript;recognition.finalTranscript='';if(spoken)sendMessage(spoken)};mic.addEventListener('click',()=>{if(listening){recognition.stop();return}try{recognition.finalTranscript='';recognition.lang=/[a-z]/i.test(promptBox.value)&&promptBox.value.trim()?'en-NG':'ha-NG';recognition.start()}catch(e){setStatus('Gwada sake dannawa')}})}else{mic.addEventListener('click',()=>{document.getElementById('voiceNote').textContent='Wannan browser ba ya goyon bayan gane magana. Ka gwada Chrome na zamani, ka tabbatar kana amfani da HTTPS, ko ka rubuta saƙon.';setStatus('Voice unsupported')})}
}
</script></body></html>'''


def is_logged_in():
    return not PASSWORD or session.get("logged_in") is True

@app.get("/")
def index():
    return render_template_string(HTML, logged_in=is_logged_in())

@app.post("/login")
def login():
    if not PASSWORD or request.form.get("password", "") == PASSWORD:
        session["logged_in"] = True
        return redirect(url_for("index"))
    return "Kalmar sirri ba daidai ba ce.", 401

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return jsonify(status="ok", service="SALIM AI dashboard")

@app.post("/api/chat")
def chat_api():
    if not is_logged_in():
        return jsonify(error="Da fatan za ka shiga dashboard da farko."), 401
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify(error="Ka rubuta ko ka faɗi saƙo."), 400
    if len(message) > 6000:
        return jsonify(error="Saƙon ya yi tsawo. Ka rage shi."), 413
    handled, result = handle_command(message)
    if not handled:
        result = ask_gemini([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ])
    # On Render, commands cannot launch native apps on the visitor's phone; return a safe clickable URL when available.
    urls = re.findall(r"https?://[^\s<>]+", result)
    return jsonify(answer=result, links=urls[:3])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
