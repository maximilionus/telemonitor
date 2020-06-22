from aiogram import Bot, Dispatcher, executor, types

from Telemonitor import helpers as h


h.init_logger()

cfg = h.TM_Config().get()
wls = h.TM_Whitelist()
api_token = cfg["api_key"]
bot = Bot(token=api_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['test'])
async def test_message(message: types.Message):
    if wls.is_whitelisted(message):
        print(str(message))
        await message.reply("Hello")

executor.start_polling(dp)
