from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import bold, code

from Telemonitor import helpers as h, \
    __version__


def run():
    # Initialization
    h.init_logger()

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

    executor.start_polling(dp)
