import logging
from os import chdir, path

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import bold, code

from telemonitor import helpers as h, __version__
from telemonitor.extensions import systemd_service
from telemonitor.helpers import TM_Whitelist, TM_ControlInlineKB, cli_arguments_parser, PARSE_MODE, STRS


def run():
    args = cli_arguments_parser()

    chdir(path.dirname(__file__))

    h.init_logger(args.verbose)
    logger = logging.getLogger(__name__)
    logger.info("Telemonitor is starting")

    cfg = h.TM_Config().get()

    if hasattr(args, 'systemd_service'):
        systemd_service.start(args.systemd_service)

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
                bold(f"Welcome to the {STRS.name} control panel"),
                reply=False,
                parse_mode=PARSE_MODE,
                reply_markup=ikb.keyboard
            )

    if cfg["enable_file_transfer"]:
        @dp.message_handler(content_types=['document', 'photo'])
        async def __file_transfer(message: types.Message):
            if TM_Whitelist.is_whitelisted(message.from_user.id):
                h.init_shared_dir()
                if message.content_type == 'document':
                    await message.document.download(path.join(h.PATH_SHARED_DIR, message.document.file_name))
                    logger.info(f'Successfully downloaded file "{message.document.file_name}" to "{path.abspath(h.PATH_SHARED_DIR)}""')
                    await message.reply(text=f"Successfully downloaded file {code(message.document.file_name)}", parse_mode=PARSE_MODE, reply=False)
                elif message.content_type == 'photo':
                    await message.photo[-1].download(h.PATH_SHARED_DIR)
                    logger.info(f'Successfully downloaded image(-s) to "{path.join(path.abspath(h.PATH_SHARED_DIR), "photos")}"')
                    await message.reply(text="Successfully downloaded image(-s)", parse_mode=PARSE_MODE, reply=False)

    print(f'Bot is starting. Version: {__version__}')
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=(lambda _: TM_Whitelist.send_to_all(bot, STRS.message_startup)) if cfg["state_notifications"] else None,
        on_shutdown=(lambda _: TM_Whitelist.send_to_all(bot, STRS.message_shutdown)) if cfg["state_notifications"] and args.dev_features else None
    )


if __name__ == "__main__":
    run()
