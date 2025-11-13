import logging

from telegram import Update
from telegram.ext import ContextTypes

from py import config_helper, tuya_helper

COMMAND_START = "start"
COMMAND_HELP = "help"
COMMAND_LOGIN = "login"
COMMAND_OPEN_PORTAL = "open"
DEBUG_PERSISTENCE = "debug_persistence"
DEBUG_PERSISTENCE_CLEAR = "debug_persistence_clear"


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    reply_text = """
    Используй /login TOKEN, чтобы авторизироваться.
    Используй /open, чтобы открыть дверь.
    """

    await update.message.reply_text(reply_text)


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check password when the command /login is issued."""
    password = update.message.text.replace("/login", "").strip()
    if len(password) == 0:
        await update.message.reply_text("Используй /login TOKEN, чтобы авторизироваться.")
    else:
        context.user_data['password'] = password
        await update.message.reply_text("Допустим")


async def open_portal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data['password'] == config_helper.BOT_ACCESS_PASSWORD:
        success, response = await tuya_helper.open_portal()
        if success:
            await update.message.reply_text("Сим-сим, откройся!")
        else:
            await update.message.reply_text("Не получилось :( " + str(response))
    else:
        await update.message.reply_text("Сначала авторизируйся с помощью /login TOKEN")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    message = "Error happened: " + str(context.error)
    if hasattr(context, 'job') and context.job is not None:
        chat_id = context.job.user_id
        message_id = 'from job'
    elif update and update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    else:
        print("Something strange is happening, no message in the update:", update)
        return

    await context.bot.send_message(chat_id=chat_id, reply_to_message_id=message_id, text=message)


async def persistence_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send message containing current persistence state."""
    await update.message.reply_text(
        "Current persistence state: \n" + str(context.user_data)
    )

async def persistence_clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send message containing current persistence state."""
    context.user_data.clear()
    await update.message.reply_text(
        "Cleared persistence."
    )