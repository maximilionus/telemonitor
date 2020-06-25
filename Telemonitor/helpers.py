import json
import logging
import os
import platform
from sys import exit, \
    platform as sys_platform
from time import strftime
import subprocess

from uptime import uptime
from aiogram import types, \
    Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ParseMode
from aiogram.utils.markdown import code, bold, italic

DIR_LOG = os.path.abspath("./Logs")
PATH_CFG = os.path.abspath("./config.json")
PARSE_MODE = ParseMode.MARKDOWN_V2
DEF_CFG = {
    "api_key": "",
    "whitelisted_users": []
}


def init_logger():
    if not os.path.isdir(DIR_LOG):
        os.makedirs(DIR_LOG)
    filename = f'{DIR_LOG}/TMLog_{strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=filename, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")


def construct_sysinfo() -> str:
    __uname = platform.uname()
    __sysname = __uname[0]
    __architecture = __uname[4]
    __uptime_raw = uptime()
    __uptime = f"{int(__uptime_raw / (24 * 3600))}:{int(__uptime_raw / 3600)}:{int(__uptime_raw / 60 % 60)}:{int(__uptime_raw % 60)}"
    __userhost = f"{os.path.basename(os.path.expanduser('~'))}@{__uname[1]}"

    string_final = f"{bold('System')}: {code(__sysname)}\n{bold('Architecture')}: {code(__architecture)}\n{bold('Uptime')} {italic('dd:hh:mm:ss')}: {code(__uptime)}\n{bold('User@Host')}: {code(__userhost)}"
    return string_final


class TM_ControlInlineKB:
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        self.inline_kb = InlineKeyboardMarkup()
        self.btn_get_sysinfo = InlineKeyboardButton('Sys Info', callback_data='button-sysinfo-press')
        self.btn_reboot = InlineKeyboardButton('Reboot', callback_data='button-reboot-press')
        self.btn_shutdown = InlineKeyboardButton('Shutdown', callback_data='button-shutdown-press')

        self.inline_kb.add(self.btn_get_sysinfo)
        self.inline_kb.add(self.btn_reboot)
        self.inline_kb.add(self.btn_shutdown)

        @dispatcher.callback_query_handler()
        async def __callback_sysinfo_press(callback_query: types.CallbackQuery):
            cb = callback_query.data
            if cb == 'button-sysinfo-press':
                await bot.answer_callback_query(callback_query.id)
                message = construct_sysinfo()
                await bot.send_message(callback_query.from_user.id, message, parse_mode=PARSE_MODE)

            elif cb == 'button-reboot-press':
                await bot.answer_callback_query(callback_query.id)
                await bot.send_message(callback_query.from_user.id, code("Rebooting the system..."), parse_mode=PARSE_MODE)

                plf = sys_platform
                if plf == 'linux': subprocess.call(['reboot', 'now'])
                elif plf == 'win32': subprocess.call(['shutdown', '-t', '0', '-r', '-f'])

            elif cb == 'button-shutdown-press':
                await bot.answer_callback_query(callback_query.id)
                await bot.send_message(callback_query.from_user.id, code("Shutting down the system..."), parse_mode=PARSE_MODE)

                plf = sys_platform
                if plf == 'linux': subprocess.call(['shutdown', 'now'])
                elif plf == 'win32': subprocess.call(['shutdown', '-s', '-t', '0'])

    def get_keyboard(self) -> object:
        return self.inline_kb


class TM_Whitelist:
    @classmethod
    def is_whitelisted(cls, message: types.Message):
        users = cls.get_whitelist()
        if message.from_user.id in users:
            return True
        else:
            return False

    @staticmethod
    def get_whitelist():
        return TM_Config.get()["whitelisted_users"]


class TM_Config:
    __logger = logging.getLogger("TM.Config")

    def __init__(self):
        if not self.is_exist():
            self.create()
            print(f"Config file was generated in < {PATH_CFG} >.\nFirst, you need to configure its values and then run the script again.")
            exit()

    @staticmethod
    def is_exist() -> bool:
        return True if os.path.isfile(PATH_CFG) else False

    @classmethod
    def create(cls):
        with open(PATH_CFG, 'wt') as f:
            json.dump(DEF_CFG, f, indent=4)
        cls.__logger.info("Config file was generated.")

    @classmethod
    def get(cls) -> dict:
        with open(PATH_CFG, 'rt') as f:
            cfg = json.load(f)
        return cfg
