import os
import re
import uuid
import yt_dlp
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from interacted import interacted


async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    video_pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/watch\?v=[\w-]+(?:&[^\s]*)?'

    if not re.match(video_pattern, url):
        await update.message.reply_text(
            "❌ Invalid link")
        return

    await update.message.reply_text(
        "✅ Valid link")
    await update.message.reply_text(
        "⬇️ Downloading...")

    cookies_file = 'cookies.txt'

    with yt_dlp.YoutubeDL({
        'cookiefile': cookies_file,
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True
    }) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        file_size = info_dict.get('filesize', 0)

    if file_size and file_size > 50 * 1024 * 1024:
        await update.message.reply_text('Audio is too large.')
        return

    download_folder = f'downloads/{uuid.uuid4()}'
    os.makedirs(download_folder, exist_ok=True)

    file_path = f"{download_folder}/%(title)s.%(ext)s"

    with yt_dlp.YoutubeDL({
        'cookiefile': cookies_file,
        'noplaylist': True,
        'outtmpl': file_path,
        'quiet': True,
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }) as ydl:
        ydl.download([url])

    downloaded_file = None

    for root, dirs, files in os.walk(download_folder):
        for file in files:
            if file.endswith('.mp3'):
                downloaded_file = os.path.join(root, file)
                break

    if downloaded_file:
        with open(downloaded_file, 'rb') as audio_file:
            await update.message.reply_audio(audio_file)

    else:
        await update.message.reply_text("❌ Failed to download audio, please try again")

    shutil.rmtree(download_folder)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    interacted(user)

    await update.message.reply_text(
        "Hello! Send me a YouTube link to download MP3 audio ✨")


def main():
    app = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, download_audio))

    app.run_polling()


if __name__ == "__main__":
    main()
