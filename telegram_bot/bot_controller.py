"""
Main class definition for the Telegram Bot interface.
"""

import os
import logging

from telegram.ext import (
    Application,
    CommandHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler,
    InvalidCallbackData,
    MessageHandler,
)

from .handlers.command import start, help_msg, tracked_courses
from .handlers import conversation as con
from .handlers.conversation import CommandEnum
from .handlers.error import call_back_error, non_existent


# setting up the logger for the bot status
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class BotController:
    """The main entry of activating
    our telegram bot.
    It initializes all handlers"""

    def __init__(self) -> None:

        self.app: Application = (
            Application.builder()
            .token(os.environ.get("TELEGRAM_BOT_TOKEN"))
            .arbitrary_callback_data(True)  # type: ignore
            .build()
        )
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.init_comm_handlers()
        self.init_conv_handlers()
        self.app.add_handler(MessageHandler(filters.COMMAND, non_existent))
        self.app.run_polling()
        print(self.app.handlers)

        logger.info("Telegram Bot started")

    def init_comm_handlers(self) -> None:
        """Simple handlers"""

        self.app.add_handler(CommandHandler("start", start))
        self.app.add_handler(CommandHandler("help", help_msg))
        self.app.add_handler(CommandHandler("tracked", tracked_courses))
        self.app.add_handler(
            CallbackQueryHandler(call_back_error, pattern=InvalidCallbackData)
        )

        logger.info("Handlers initialized")

    def init_conv_handlers(self) -> None:
        """to handle all assigned conversation handlers"""

        track_handler = ConversationHandler(
            entry_points=[CommandHandler("track", con.track)],  # type: ignore
            states={
                CommandEnum.DEPT: [CallbackQueryHandler(con.track_dept)],
                CommandEnum.COURSE: [CallbackQueryHandler(con.track_courses)],
                CommandEnum.SECTION: [
                    CallbackQueryHandler(con.track_sections)
                ],
                CommandEnum.CRN: [MessageHandler(filters.TEXT, con.track_crn)],
                CommandEnum.CONFIRM: [CallbackQueryHandler(con.track_confirm)],
            },  # type: ignore
            fallbacks=[CommandHandler("cancel", con.cancel)],  # type: ignore
        )
        self.app.add_handler(track_handler)

        untrack_handler = ConversationHandler(
            entry_points=[CommandHandler("untrack", con.untrack)],  # type: ignore
            states={
                CommandEnum.CRN: [
                    MessageHandler(filters.TEXT, con.untrack_crn)
                ],
                CommandEnum.SELECT: [CallbackQueryHandler(con.untrack_select)],  # type: ignore
            },
            fallbacks=[CommandHandler("cancel", con.cancel)],  # type: ignore
        )
        self.app.add_handler(untrack_handler)

        clear_handler = ConversationHandler(
            entry_points=[CommandHandler("clear", con.clear)],  # type: ignore
            states={
                CommandEnum.CONFIRM: [CallbackQueryHandler(con.clear_confirm)]  # type: ignore
            },
            fallbacks=[CommandHandler("cancel", con.cancel)],
        )
        self.app.add_handler(clear_handler)
