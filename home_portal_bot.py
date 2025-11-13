#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import asyncio
import io
import logging
import sys
from pathlib import Path

from telegram import __version__ as TG_VER, BotCommand, Voice, Audio, File, Document

from py import commands, config_helper

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    PicklePersistence
)

# Enable logging
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def handle_message(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    result = ask_with_function_calling(context.user_data, text)

    context.user_data["previous_message"] = text
    context.user_data["previous_result"] = result
    return result


async def ask_ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("password") != config_helper.CHATBOT_ACCESS_PASSWORD:
        await commands.help_command(update, context)
        return

    text = update.message.text

    audio: Voice | Audio | None = update.message.audio or update.message.voice
    if not text and audio:
        file: File = await context.bot.get_file(audio)
        bytes_array: bytearray = await file.download_as_bytearray()
        bytes_type = bytes(bytes_array)
        byteio = io.BytesIO(bytes_array)
        byteio.name = "file.oga"

        text = openai_conversation_helper.transcribe_voice_message(bytes_type)
        print("Transcribed text:", text)

    response = handle_message(text, update, context)
    await update.message.reply_text(response)


async def with_document_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("password") != config_helper.CHATBOT_ACCESS_PASSWORD:
        await commands.help_command(update, context)
        return

    text = update.message.text

    document: Document | None = update.message.document

    file: File = await context.bot.get_file(document)

    file_path: Path = await file.download_to_drive(custom_path=document.file_name)
    file_streams = [open(file_path, "rb")]
    vector_store_id = get_vector_store_id(context.user_data)

    file_batch: VectorStoreFileBatch = openai_conversation_helper.client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
    )
    logger.debug(f"File batch upload result: {file_batch}")
    if file_batch.file_counts.failed > 0:
        response = "Ошибка загрузки файла"
    elif text:
        response = handle_message(text, update, context)
    else:
        response = "Файл успешно загружен"

    await update.message.reply_text(response)



# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/persistentconversationbot.py
def main() -> None:

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="persistence", update_interval=5)
    application = Application.builder().job_queue(None).token(config_helper.TELEGRAM_TOKEN).persistence(persistence).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(commands.COMMAND_START, commands.help_command))
    application.add_handler(CommandHandler(commands.COMMAND_HELP, commands.help_command))
    application.add_handler(CommandHandler(commands.COMMAND_LOGIN, commands.login_command))
    application.add_handler(CommandHandler(commands.COMMAND_OPEN_PORTAL, commands.open_portal_command))
    application.add_handler(CommandHandler(commands.DEBUG_PERSISTENCE, commands.persistence_command))
    application.add_handler(CommandHandler(commands.DEBUG_PERSISTENCE_CLEAR, commands.persistence_clear_command))

    command = [
        BotCommand(commands.COMMAND_HELP, "See explanations"),
        BotCommand(commands.COMMAND_LOGIN, "/login TOKEN"),
        BotCommand(commands.COMMAND_OPEN_PORTAL, "Повернись к лесу задом, ко мне передом"),
    ]
    asyncio.ensure_future(application.bot.set_my_commands(command))

    application.add_error_handler(commands.error_handler)

    # on non command i.e message
    application.add_handler(MessageHandler(filters.Document.APPLICATION | filters.Document.TEXT, with_document_command))
    application.add_handler(MessageHandler(filters.TEXT | filters.AUDIO | filters.VOICE, ask_ai_command))
    # application.add_handler(MessageHandler(filters.AUDIO & ~filters.COMMAND, ask_ai_voice_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    # print("=====================BEGINNING===============")
    # print(sys.getdefaultencoding())
    # import locale
    # print(locale.getdefaultlocale())
    # locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    # print(locale.getdefaultlocale())
    # print("Проверка настроек локали")
    main()
