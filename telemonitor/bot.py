import logging
import platform
import subprocess
from os import path
from math import floor
from sys import platform as sys_platform

from uptime import uptime
from aiogram.utils.markdown import bold, code, italic
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from . import __version__
from .core import constants
from .core.cli import tm_colorama
from .core.io import TM_Config, TM_Whitelist, init_shared_dir


def start_telegram_bot():
    from telemonitor.__main__ import args

    logger = logging.getLogger(__name__)
    colorama = tm_colorama()
    cfg = TM_Config.get()
    api_token = cfg["bot"]["token"] if args.token_overwrite is None else args.token_overwrite

    bot = Bot(token=api_token)
    dp = Dispatcher(bot)

    # Inline keyboard for controls
    ikb = main_inline_kb(bot, dp)

    # Handlers
    @dp.message_handler(commands=['start'])
    async def __command_start(message: types.Message):
        if TM_Whitelist.is_whitelisted(message.from_user.id):
            await message.reply(
                bold(f"Welcome to the {constants.STRS.name} control panel"),
                reply=False,
                parse_mode=constants.PARSE_MODE,
                reply_markup=ikb
            )

    if cfg["bot"]["enable_file_transfer"]:
        @dp.message_handler(content_types=['document', 'photo'])
        async def __file_transfer(message: types.Message):
            if TM_Whitelist.is_whitelisted(message.from_user.id):
                init_shared_dir()

                if message.content_type == 'document':
                    await message.document.download(path.join(constants.PATH_SHARED_DIR, message.document.file_name))
                    logger.info(f'Successfully downloaded file "{message.document.file_name}" to "{path.abspath(constants.PATH_SHARED_DIR)}""')
                    await message.reply(text=f"Successfully downloaded file {code(message.document.file_name)}", parse_mode=constants.PARSE_MODE, reply=False)

                elif message.content_type == 'photo':
                    await message.photo[-1].download(constants.PATH_SHARED_DIR)
                    logger.info(f'Successfully downloaded image(-s) to "{path.join(path.abspath(constants.PATH_SHARED_DIR), "photos")}"')
                    await message.reply(text="Successfully downloaded image(-s)", parse_mode=constants.PARSE_MODE, reply=False)

    print(f'{colorama.Fore.CYAN}{constants.STRS.name}{colorama.Style.RESET_ALL} is starting. Version: {colorama.Fore.CYAN}{__version__}{colorama.Style.RESET_ALL}')
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=(lambda _: TM_Whitelist.send_to_all(bot, constants.STRS.message_startup)) if cfg["bot"]["state_notifications"] else None,
        on_shutdown=(lambda _: TM_Whitelist.send_to_all(bot, constants.STRS.message_shutdown)) if cfg["bot"]["state_notifications"] and args.dev_features else None
    )


def main_inline_kb(bot, dispatcher):
    """ Generate telegram inline keyboard for bot.

    Args:
        bot (Bot): aiogram Bot object.
        dispatcher (Dispatcher): aiogram Dispatcher object.
    """
    inline_kb = InlineKeyboardMarkup()

    btn_get_sysinfo = InlineKeyboardButton('Sys Info', callback_data='button-sysinfo-press')
    btn_reboot = InlineKeyboardButton('Reboot', callback_data='button-reboot-press')
    btn_shutdown = InlineKeyboardButton('Shutdown', callback_data='button-shutdown-press')

    inline_kb.add(btn_get_sysinfo)
    inline_kb.row(btn_reboot, btn_shutdown)

    @dispatcher.callback_query_handler()
    async def __callback_ctrl_press(callback_query: types.CallbackQuery):
        if not TM_Whitelist.is_whitelisted(callback_query.from_user.id): return False

        data = callback_query.data
        if data == 'button-sysinfo-press':
            await bot.answer_callback_query(callback_query.id)
            message = construct_sysinfo()
            await bot.send_message(callback_query.from_user.id, message, parse_mode=constants.PARSE_MODE)

        elif data == 'button-reboot-press':
            await bot.answer_callback_query(callback_query.id, constants.STRS.reboot, show_alert=True)

            if sys_platform == 'linux': subprocess.run(['shutdown', '-r', 'now'])
            elif sys_platform == 'darwin': subprocess.run(['shutdown', '-r', 'now'])
            elif sys_platform == 'win32': subprocess.run(['shutdown', '/r', '/t', '0'])

        elif data == 'button-shutdown-press':
            await bot.answer_callback_query(callback_query.id, constants.STRS.shutdown, show_alert=True)

            if sys_platform == 'linux': subprocess.run(['shutdown', 'now'])
            elif sys_platform == 'darwin': subprocess.run(['shutdown', '-h', 'now'])
            elif sys_platform == 'win32': subprocess.run(['shutdown', '/s', '/t', '0'])

    return inline_kb


def construct_sysinfo() -> str:
    """ Get system information and construct message from it.

    Returns:
        str: Constructed and formatted message, ready for Telegram.
    """
    __uname = platform.uname()
    __sysname = f"{__uname.system} {__uname.release} ({__uname.version})"
    __userhost = f"{path.basename(path.expanduser('~'))}@{__uname.node}"

    __uptime_raw = uptime()
    __uptime_dict = {
        "days": str(floor(__uptime_raw / (24 * 3600))),
        "hours": str(floor(__uptime_raw / 3600)),
        "mins": str(floor(__uptime_raw / 60 % 60)),
        "secs": str(floor(__uptime_raw % 60))
    }
    __uptime_dict.update({k: f"0{__uptime_dict[k]}" for k in __uptime_dict if len(__uptime_dict[k]) == 1})
    __uptime = f"{__uptime_dict['days']}:{__uptime_dict['hours']}:{__uptime_dict['mins']}:{__uptime_dict['secs']}"

    string_final = f"{bold('System')}: {code(__sysname)}\n{bold('Uptime')} {italic('dd:hh:mm:ss')}: {code(__uptime)}\n{bold('User@Host')}: {code(__userhost)}"
    return string_final
