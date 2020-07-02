from os import chdir, path
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import bold, code

from Telemonitor import helpers as h, __version__
from Telemonitor.helpers import TM_Config, TM_Whitelist, TM_ControlInlineKB


def run():
    chdir(path.dirname(__file__))
    h.init_logger()
    logger = logging.getLogger('TM.Main')
    logger.info("Bot is starting")

    cfg = TM_Config().get()
    api_token = cfg["api_key"]
    bot = Bot(token=api_token)
    dp = Dispatcher(bot)

    # Inline keyboard for controls
    ikb = TM_ControlInlineKB(bot, dp)

    # Handlers
    @dp.message_handler(commands=['start'])
    async def __command_start(message: types.Message):
        if TM_Whitelist.is_whitelisted(message.from_user.id):
            await message.reply(
                bold("Welcome to the Telemonitor control panel"),
                reply=False,
                parse_mode=h.PARSE_MODE,
                reply_markup=ikb.get_keyboard()
            )

    print(f'Bot is starting. Version: {__version__}')
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=lambda _: TM_Whitelist.send_to_all(bot, code("System was booted")),
        on_shutdown=lambda _: TM_Whitelist.send_to_all(bot, code("System is shutting down"))
    )
