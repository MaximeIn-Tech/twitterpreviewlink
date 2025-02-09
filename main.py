import logging
import os
import re
import socket
import unicodedata

from dotenv import load_dotenv
from httpcore import ConnectError
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="logs.log",
    encoding="utf-8",
    filemode="a",
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Initiate the bot token and chat_id as a variable. The token is stored in a .env file.
token = os.getenv("TOKEN_BOT")


async def start(update, context):
    """Handle the /help command."""
    await update.message.reply_text(
        """Hello! Send your link and you'll get a link that has a preview! Enjoy!
"""
    )


async def get_twitter_link(update, context):
    """Handle incoming messages and modify Twitter/X links."""
    if update.message.text:
        user_message = update.message.text
    elif update.message.caption:
        user_message = update.message.caption
    else:
        return

    # Regex pattern to match Twitter/X URLs
    pattern = re.compile(r"https://x\.com/\S+/status/\d+")
    match = pattern.search(user_message)

    if match:
        modified_link = match.group() + "?=19"
        await update.message.reply_text(modified_link)


def main():
    """Run the bot."""
    print("Starting bot...")
    application = Application.builder().token(token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Message handler for reversing text
    application.add_handler(
        MessageHandler(
            (filters.TEXT) & ~filters.COMMAND,
            get_twitter_link,
        )
    )

    try:
        application.run_polling()
    except ConnectError as e:
        logger.error(f"Connection error: {e}")
    except socket.gaierror as e:
        logger.error(f"Hostname resolution error: {e}")


if __name__ == "__main__":
    main()
