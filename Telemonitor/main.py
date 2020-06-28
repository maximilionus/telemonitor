from os import chdir, path
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import bold, code

from Telemonitor import helpers as h, \
    __version__


def run():
    async def on_start_message():
        for user in wls.get_whitelist():
            try:
                await bot.send_message(user, code("System is booted"), parse_mode=h.PARSE_MODE)
            except Exception as e:
                logger.error(f"Can't send on-start message to user [{user}]: < {e} >")

    # Initialization
    chdir(path.dirname(__file__))
    h.init_logger()
    logger = logging.getLogger('TM.Main')

    cfg = h.TM_Config().get()
    wls = h.TM_Whitelist()
    api_token = cfg["api_key"]
    bot = Bot(token=api_token)
    dp = Dispatcher(bot)

    # Inline keyboard for controls
    ikb = h.TM_ControlInlineKB(bot, dp)

    # Handlers
    @dp.message_handler(commands=['start'])
    async def __command_start(message: types.Message):
        if wls.is_whitelisted(message.from_user.id):
            await message.reply(
                f'{bold("Welcome to the Telemonitor control panel.")}\nVersion: {code(__version__)}\n',
                reply=False,
                parse_mode=h.PARSE_MODE,
                reply_markup=ikb.get_keyboard()
            )

    print('Bot is starting')
    logger.info("Bot is starting")
    dp.loop.create_task(on_start_message())
    executor.start_polling(dp, skip_updates=True)
