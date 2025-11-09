import asyncio
import threading
from flask import Flask
from bot.main import main as run_telegram_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram bot server is running fine!"

def start_bot():
    """Start the Telegram bot in its own asyncio loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_telegram_bot())
    loop.close()

if __name__ == "__main__":
    # Run Telegram bot in a background thread
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    # Run Flask web app (for Render uptime pings)
    app.run(host="0.0.0.0", port=10000)
