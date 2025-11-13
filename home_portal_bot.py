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
    application.add_handler(MessageHandler(~filters.COMMAND, commands.help_command))

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
