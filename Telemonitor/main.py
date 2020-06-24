from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import bold, code
from aiogram.types import ParseMode

from Telemonitor import helpers as h
from Telemonitor import __version__


PARSE_MODE = ParseMode.MARKDOWN_V2

h.init_logger()

cfg = h.TM_Config().get()
wls = h.TM_Whitelist()
api_token = cfg["api_key"]
bot = Bot(token=api_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def __command_start(message: types.Message):
    if wls.is_whitelisted(message):
        await bot.send_message(
            message.from_user.id, f'{bold("Welcome to the Telemonitor control panel.")}\nVersion: {code(__version__)}\n',
            parse_mode=PARSE_MODE
        )

executor.start_polling(dp)
