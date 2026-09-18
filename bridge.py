# -*- coding: utf-8 -*-
import asyncio, json, os, subprocess, sys, time, uuid
from pathlib import Path
from aiohttp import web
from botpy import Client, Intents
import yaml

BASE = Path(__file__).parent
def cfg():
    d = {}
    for f in [BASE / "config.yaml", BASE / "config.local.yaml"]:
        if f.exists():
            ov = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            _u(d, ov)
    return d
def _u(d, u):
    for k,v in u.items():
        if isinstance(v,dict) and isinstance(d.get(k),dict): _u(d[k],v)
        else: d[k]=v
C = cfg()

def run_codex(msg):
    cc = C.get("codex", {})
    ws = cc.get("workspace", os.getcwd())
    tmp = Path(BASE / (cc.get("temp_dir", "./temp")))
    tmp.mkdir(parents=True, exist_ok=True)
    out = tmp / ("c" + uuid.uuid4().hex[:8] + ".txt")
    cmd = ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox", "-C", ws, "-o", str(out), "--json",
           "[Reply in Chinese conversationally] " + msg]
    print("[Codex] " + msg[:80])
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=90, cwd=ws, encoding="utf-8", errors="replace")
        print("[Codex] rc=" + str(p.returncode) + " out=" + str(len(p.stdout or "")))
        reply = out.read_text(encoding="utf-8", errors="replace").strip() if out.exists() else ""
        if not reply and p.stderr: reply = p.stderr.strip()[:2000]
        if not reply:
            for line in reversed((p.stdout or "").splitlines()):
                try: reply = json.loads(line).get("text") or json.loads(line).get("content") or ""; break
                except: pass
        if p.returncode != 0 and not reply: reply = "[Codex error] rc=" + str(p.returncode)
        # Patch session source: exec -> vscode so desktop shows it
        try:
            sp = Path(os.path.expandvars("%USERPROFILE%")).joinpath(".codex/sessions")
            now = time.time()
            for y in sp.iterdir():
                if not y.is_dir(): continue
                for m in y.iterdir():
                    if not m.is_dir(): continue
                    for d2 in m.iterdir():
                        if not d2.is_dir(): continue
                        for f in d2.iterdir():
                            if f.suffix == ".jsonl" and abs(f.stat().st_mtime - now) < 120:
                                tx = f.read_text(encoding="utf-8")
                                if chr(34) + "source" + chr(34) + ": " + chr(34) + "exec" + chr(34) in tx:
                                    tx = tx.replace(chr(34)+"source"+chr(34)+": "+chr(34)+"exec"+chr(34),
                                                     chr(34)+"source"+chr(34)+": "+chr(34)+"vscode"+chr(34))
                                    f.write_text(tx, encoding="utf-8")
                                    print("[Patch] " + f.name[:50])
        except: pass
        return reply or "(empty)"
    except subprocess.TimeoutExpired: return "[Timeout 90s]"
    except Exception as e: return "[Error: " + str(e) + "]"

def split(t, lim=4000):
    if len(t) <= lim: return [t]
    r = []
    while len(t) > lim:
        c = t.rfind("\n", 0, lim)
        if c < lim//2: c = lim
        r.append(t[:c]); t = t[c:].lstrip()
    if t: r.append(t); return r

class B(Client):
    def __init__(self): super().__init__(intents=Intents(direct_message=True, public_messages=True))
    async def on_ready(self): print("[Bot] Ready!")
    async def on_c2c_message_create(self, msg):
        au = getattr(msg, "author", None)
        uid = str(getattr(au, "id", "") or getattr(au, "user_openid", ""))
        ct = str(getattr(msg, "content", "")).strip()
        al = [str(u) for u in C.get("auth",{}).get("allowed_users",[])]
        if al and al != ["0"] and uid not in al: return
        asyncio.create_task(self._on_msg(uid, ct))
    async def start_wh(self, port=9000):
        a = web.Application(); a.router.add_post("/qqbot", self._wh)
        r = web.AppRunner(a); await r.setup()
        s = web.TCPSite(r, "0.0.0.0", port); await s.start()
        print("[Webhook] :" + str(port))
    async def _wh(self, req):
        try:
            d = await req.json()
            if d.get("op")==0 and d.get("t")=="C2C_MESSAGE_CREATE":
                a = d["d"].get("author",{})
                uid = str(a.get("user_openid","") or a.get("id",""))
                ct = d["d"].get("content","")
                al = [str(u) for u in C.get("auth",{}).get("allowed_users",[])]
                if not al or al==["0"] or uid in al:
                    asyncio.create_task(self._on_msg(uid, ct))
        except: pass
        return web.json_response({"code":0})
    async def _on_msg(self, uid, ct):
        print("[MSG] " + uid[:16] + "...: " + ct[:100])
        if ct.strip() in ["/new","/n"]: await self._reply(uid,"New chat."); return
        await self._reply(uid, "Thinking...")
        r = await asyncio.get_event_loop().run_in_executor(None, run_codex, ct.strip())
        for i, p in enumerate(split(r)):
            tag = ""
            if len(split(r))>1: tag = "("+str(i+1)+"/"+str(len(split(r)))+")\n"
            await self._reply(uid, tag + (r if i==0 else p))
        print("[Send] OK")
    async def _reply(self, uid, t):
        try: await self.api.post_c2c_message(openid=uid, msg_type=0, content=t)
        except Exception as e: print("[SendErr] "+str(e))

async def main():
    q = C.get("qq_bot",{}); aid,sec = q.get("app_id",""), q.get("app_secret","")
    if not aid or not sec: print("Configure app_id/app_secret"); return
    print("QQ-Codex Bridge\n  AppID: " + aid + "  Work: " + C.get("codex",{}).get("workspace","."))
    b = B()
    await b.start_wh(port=q.get("webhook_port",9000))
    try:
        from pyngrok import ngrok, conf
        tk = q.get("ngrok_token","")
        if tk: conf.get_default().auth_token = tk
        t = ngrok.connect(9000,"http")
        print("[ngrok] >>> " + t.public_url + "/qqbot")
    except Exception as e: print("[ngrok] " + str(e))
    print("[Bot] Connecting...")
    async with b: await b.start(appid=aid, secret=sec); await asyncio.Event().wait()

if __name__ == "__main__":
    if sys.platform == "win32": asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try: asyncio.run(main())
    except KeyboardInterrupt: print("\nBye")
