from flask import Flask
import threading
import bot.main  # import your bot logic

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    bot.main.main()  # make sure your main() starts the Telegram bot

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
