#!/usr/bin/env python3
"""LINE Messaging API webhook handler for Smith (Work).

Runs a local HTTP server, receives webhook events from LINE,
validates signatures, and routes commands to handlers.

Usage:
  source ~/.config/smith/.env
  python3 skills/line/handler.py
"""

import base64
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

# --- Config ---
CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
PORT = int(os.environ.get("LINE_WEBHOOK_PORT", "8080"))
OWNER_USER_IDS = set(
    x.strip()
    for x in os.environ.get("LINE_OWNER_USER_IDS", "").split(",")
    if x.strip()
)

API_BASE = "https://api.line.me"


# --- API helpers ---
def _headers():
    return {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }


def reply(reply_token: str, text: str) -> dict:
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}],
    }
    req = urllib.request.Request(
        f"{API_BASE}/v2/bot/message/reply",
        data=json.dumps(payload).encode(),
        headers=_headers(),
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode() or "{}")
    except Exception as e:
        print(f"[reply] failed: {e}", file=sys.stderr)
        return {"ok": False, "error": str(e)}


def push(user_id: str, text: str) -> dict:
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": text}],
    }
    req = urllib.request.Request(
        f"{API_BASE}/v2/bot/message/push",
        data=json.dumps(payload).encode(),
        headers=_headers(),
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode() or "{}")
    except Exception as e:
        print(f"[push] failed: {e}", file=sys.stderr)
        return {"ok": False, "error": str(e)}


def get_bot_info() -> dict:
    req = urllib.request.Request(
        f"{API_BASE}/v2/bot/info",
        headers=_headers(),
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode() or "{}")
    except Exception as e:
        print(f"[get_bot_info] failed: {e}", file=sys.stderr)
        return {"ok": False, "error": str(e)}


# --- Signature validation ---
def validate_signature(body: bytes, signature: str) -> bool:
    if not CHANNEL_SECRET:
        return False
    mac = hmac.new(CHANNEL_SECRET.encode(), body, hashlib.sha256)
    expected = base64.b64encode(mac.digest()).decode()
    return hmac.compare_digest(expected, signature)


# --- Command handlers ---
def on_start(reply_token: str, _user_id: str) -> None:
    reply(
        reply_token,
        "Smith (Work) is online on LINE.\n"
        "Type /help to see commands.",
    )


def on_help(reply_token: str, _user_id: str) -> None:
    reply(
        reply_token,
        "Commands:\n"
        "/start - intro\n"
        "/help - this\n"
        "/status - health & memory\n"
        "/briefing - morning/evening digest\n"
        "/tasks - todoist today/overdue\n"
        "/traffic - commute traffic\n"
        "/email - unread agentmail count\n"
        "/ping - quick health check",
    )


def on_status(reply_token: str, _user_id: str) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    reply(
        reply_token,
        f"Status\n\n"
        f"- time: {now}\n"
        f"- channel: LINE\n"
        f"- env: {'set' if CHANNEL_ACCESS_TOKEN else 'MISSING'}",
    )


def on_ping(reply_token: str, _user_id: str) -> None:
    reply(reply_token, "pong")


def on_briefing(reply_token: str, _user_id: str) -> None:
    reply(reply_token, "Briefing feature placeholder - integrate with morning-briefing skill later.")


def on_tasks(reply_token: str, _user_id: str) -> None:
    reply(reply_token, "Tasks feature placeholder - integrate with todoist skill later.")


def on_traffic(reply_token: str, _user_id: str) -> None:
    reply(reply_token, "Traffic feature placeholder - integrate with TomTom skill later.")


def on_email(reply_token: str, _user_id: str) -> None:
    reply(reply_token, "Email feature placeholder - integrate with AgentMail skill later.")


COMMANDS = {
    "/start": on_start,
    "/help": on_help,
    "/status": on_status,
    "/ping": on_ping,
    "/briefing": on_briefing,
    "/tasks": on_tasks,
    "/traffic": on_traffic,
    "/email": on_email,
}


# --- Webhook handler ---
def handle_events(events: list) -> None:
    for event in events:
        etype = event.get("type")
        if etype != "message":
            continue

        msg = event.get("message", {})
        if msg.get("type") != "text":
            continue

        text = (msg.get("text") or "").strip()
        reply_token = event.get("replyToken", "")
        user_id = event.get("source", {}).get("userId", "")
        source_type = event.get("source", {}).get("type", "")

        print(f"[event] {source_type}:{user_id} -> {text[:80]}", file=sys.stderr)

        if not text.startswith("/"):
            # Non-command messages - optional: forward to opencode/Smith
            continue

        command = text.split()[0].split("@")[0]
        handler = COMMANDS.get(command)
        if handler:
            try:
                handler(reply_token, user_id)
            except Exception as e:
                print(f"[handler] {command} failed: {e}", file=sys.stderr)
        else:
            reply(reply_token, f"Unknown: {command}\n/help for commands.")


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        signature = self.headers.get("X-Line-Signature", "")

        if not validate_signature(body, signature):
            print("[webhook] invalid signature", file=sys.stderr)
            self.send_response(403)
            self.end_headers()
            return

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        events = data.get("events", [])
        handle_events(events)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            info = {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}
            self.wfile.write(json.dumps(info).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[http] {format % args}", file=sys.stderr)


def main():
    if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
        print("Set LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN first.", file=sys.stderr)
        print("  source ~/.config/smith/.env", file=sys.stderr)
        sys.exit(1)

    # Verify bot info
    info = get_bot_info()
    if info.get("displayName"):
        print(f"[bot] connected as: {info['displayName']}", file=sys.stderr)
    else:
        print("[bot] could not verify bot info - check credentials", file=sys.stderr)

    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    print(f"[webhook] listening on :{PORT}/", file=sys.stderr)
    print(f"[webhook] health check: GET /health", file=sys.stderr)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[webhook] stopped.", file=sys.stderr)
        server.server_close()


if __name__ == "__main__":
    main()
