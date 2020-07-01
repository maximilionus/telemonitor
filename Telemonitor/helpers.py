import json
import logging
import os
import platform
from sys import platform as sys_platform
from time import strftime
import subprocess

from uptime import uptime
from aiogram import types, Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils.markdown import code, bold, italic


MAX_LOGS = 30
DIR_LOG = "./Logs"
PATH_CFG = "./config.json"
PARSE_MODE = ParseMode.MARKDOWN_V2
DEF_CFG = {
    "api_key": "",
    "whitelisted_users": []
}


def init_logger():
    if not os.path.isdir(DIR_LOG):
        os.makedirs(DIR_LOG)
    else:
        log_files = [f for f in os.listdir(DIR_LOG) if os.path.isfile(os.path.join(DIR_LOG, f))]
        log_files_len = len(log_files)
        if log_files_len > MAX_LOGS:
            print(f"Clearing logs folder. {log_files_len} files will be removed")
            for log_file in log_files:
                os.remove(os.path.join(DIR_LOG, log_file))
    filename = f'{DIR_LOG}/TMLog_{strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=filename, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")


def construct_sysinfo() -> str:
    __uname = platform.uname()
    __sysname = f"{__uname[0]} {__uname[4]}"
    __uptime_raw = uptime()
    __uptime = f"{int(__uptime_raw / (24 * 3600))}:{int(__uptime_raw / 3600)}:{int(__uptime_raw / 60 % 60)}:{int(__uptime_raw % 60)}"
    __userhost = f"{os.path.basename(os.path.expanduser('~'))}@{__uname[1]}"

    string_final = f"{bold('System')}: {code(__sysname)}\n{bold('Uptime')} {italic('dd:hh:mm:ss')}: {code(__uptime)}\n{bold('User@Host')}: {code(__userhost)}"
    return string_final


class TM_ControlInlineKB:
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        self.inline_kb = InlineKeyboardMarkup()

        self.btn_get_sysinfo = InlineKeyboardButton('Sys Info', callback_data='button-sysinfo-press')
        self.btn_reboot = InlineKeyboardButton('Reboot', callback_data='button-reboot-press')
        self.btn_shutdown = InlineKeyboardButton('Shutdown', callback_data='button-shutdown-press')

        self.inline_kb.add(self.btn_get_sysinfo)
        self.inline_kb.row(self.btn_reboot, self.btn_shutdown)

        @dispatcher.callback_query_handler()
        async def __callback_sysinfo_press(callback_query: types.CallbackQuery):
            if not TM_Whitelist.is_whitelisted(callback_query.from_user.id): return False

            data = callback_query.data
            if data == 'button-sysinfo-press':
                await bot.answer_callback_query(callback_query.id)
                message = construct_sysinfo()
                await bot.send_message(callback_query.from_user.id, message, parse_mode=PARSE_MODE)

            elif data == 'button-reboot-press':
                await bot.answer_callback_query(callback_query.id, 'Rebooting the system...')

                if sys_platform == 'linux': subprocess.run(['shutdown', '-r', 'now'])
                elif sys_platform == 'darwin': subprocess.run(['shutdown', '-r', 'now'])
                elif sys_platform == 'win32': subprocess.run(['shutdown', '/r', '/t', '0'])

            elif data == 'button-shutdown-press':
                await bot.answer_callback_query(callback_query.id, "Shutting down the system...")

                if sys_platform == 'linux': subprocess.run(['shutdown', 'now'])
                elif sys_platform == 'darwin': subprocess.run(['shutdown', '-h', 'now'])
                elif sys_platform == 'win32': subprocess.run(['shutdown', '/s', '/t', '0'])

    def get_keyboard(self) -> object:
        return self.inline_kb


class TM_Whitelist:
    __logger = logging.getLogger("TM.Whitelist")

    @classmethod
    def is_whitelisted(cls, user_id: int):
        users = cls.get_whitelist()
        if user_id in users:
            return True
        else:
            return False

    @staticmethod
    def get_whitelist():
        return TM_Config.get()["whitelisted_users"]

    @classmethod
    async def send_to_all(cls, bot: object, message: str):
        """ Send message to all users in whitelist

        Args:
            bot (object): aiogram bot object
            message (str): Text of the message

        Returns:
            None
        """
        for user in cls.get_whitelist():
            try:
                await bot.send_message(user, message, parse_mode=PARSE_MODE)
            except Exception as e:
                cls.__logger.error(f"Can't send message to whitelisted user [{user}]: < {e} >")


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
