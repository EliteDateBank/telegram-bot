import asyncio
from flask import Flask
from bot.main import main as run_telegram_bot

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Telegram Bot is running on Render!'

if __name__ == '__main__':
    # Run Telegram bot inside the same event loop
    loop = asyncio.get_event_loop()
    loop.create_task(run_telegram_bot())
    app.run(host='0.0.0.0', port=10000)
