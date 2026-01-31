import os
import telebot
import requests

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 Salom! Qo‘shiq yuboring.")

@bot.message_handler(content_types=["audio"])
def audio(message):
    audio = message.audio

    if not audio.performer or not audio.title:
        bot.send_message(message.chat.id, "❌ Audio nomi topilmadi.")
        return

    artist = audio.performer
    title = audio.title

    bot.send_message(message.chat.id, f"🔍 {artist} - {title}")

    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    r = requests.get(url)

    if r.status_code != 200:
        bot.send_message(message.chat.id, "❌ Matn topilmadi.")
        return

    lyrics = r.json().get("lyrics")

    for i in range(0, len(lyrics), 4000):
        bot.send_message(message.chat.id, lyrics[i:i+4000])

bot.infinity_polling()
