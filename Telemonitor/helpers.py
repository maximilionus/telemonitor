import json
import logging
import os
import platform
from math import floor
from sys import platform as sys_platform
from time import strftime
import subprocess

from uptime import uptime
from aiogram import types, Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils.markdown import code, bold, italic

from Telemonitor import __version__


MAX_LOGS = 30
DIR_LOG = "./Logs"
PATH_CFG = "./config.json"
PATH_SHARED_DIR = "./Shared"
PARSE_MODE = ParseMode.MARKDOWN_V2
DEF_CFG = {
    "api_key": "",
    "whitelisted_users": [],
    "log_files_max": MAX_LOGS,
    "state_notifications": True,
    "enable_file_transfer": True
}


class STRS:
    name = "Telemonitor"
    description = "Telegram bot for monitoring your system."
    reboot = "Rebooting the system"
    shutdown = "Shutting down the system"
    message_startup = code("System was booted")
    message_shutdown = code("System is shutting down")


def init_logger(is_verbose: bool = False):
    """ Initialize python `logging` module

    Args:
        is_verbose (bool, optional): Write more detailed information to log file. Defaults to False.
    """
    if not os.path.isdir(DIR_LOG):
        os.makedirs(DIR_LOG)
    else:
        log_files = [f for f in os.listdir(DIR_LOG) if os.path.isfile(os.path.join(DIR_LOG, f))]
        log_files_len = len(log_files)
        if log_files_len > (TM_Config.get().get("log_files_max", MAX_LOGS) if TM_Config.is_exist() else MAX_LOGS):
            print(f"Clearing logs folder. {log_files_len} files will be removed")
            for log_file in log_files:
                os.remove(os.path.join(DIR_LOG, log_file))

    log_level = logging.DEBUG if is_verbose else logging.INFO
    filename = f'{DIR_LOG}/TMLog_{strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=filename, format=f"[%(asctime)s][{STRS.name}:{__version__}][%(name)s][%(levelname)s]: %(message)s", level=log_level)


def construct_sysinfo() -> str:
    """ Get system information and construct message from it.

    Returns:
        str: Constructed and formatted message, ready for Telegram.
    """
    __uname = platform.uname()
    __sysname = f"{__uname.system} {__uname.release} ({__uname.version})"
    __userhost = f"{os.path.basename(os.path.expanduser('~'))}@{__uname.node}"

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


def init_shared_dir() -> bool:
    """ Initialize dir for shared files

    Returns:
        bool:
            True - Dir doesn't exist and was created.
            False - Dir already exists.
    """
    if not os.path.exists(PATH_SHARED_DIR):
        os.makedirs(PATH_SHARED_DIR)
        return True
    else:
        return False


class TM_ControlInlineKB:
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        """ Generate telegram inline keyboard for bot.

        Args:
            bot (Bot): aiogram Bot object.
            dispatcher (Dispatcher): aiogram Dispatcher object.
        """
        self.__inline_kb = InlineKeyboardMarkup()

        self.__btn_get_sysinfo = InlineKeyboardButton('Sys Info', callback_data='button-sysinfo-press')
        self.__btn_reboot = InlineKeyboardButton('Reboot', callback_data='button-reboot-press')
        self.__btn_shutdown = InlineKeyboardButton('Shutdown', callback_data='button-shutdown-press')

        self.__inline_kb.add(self.__btn_get_sysinfo)
        self.__inline_kb.row(self.__btn_reboot, self.__btn_shutdown)

        @dispatcher.callback_query_handler()
        async def __callback_ctrl_press(callback_query: types.CallbackQuery):
            if not TM_Whitelist.is_whitelisted(callback_query.from_user.id): return False

            data = callback_query.data
            if data == 'button-sysinfo-press':
                await bot.answer_callback_query(callback_query.id)
                message = construct_sysinfo()
                await bot.send_message(callback_query.from_user.id, message, parse_mode=PARSE_MODE)

            elif data == 'button-reboot-press':
                await bot.answer_callback_query(callback_query.id, STRS.reboot, show_alert=True)

                if sys_platform == 'linux': subprocess.run(['shutdown', '-r', 'now'])
                elif sys_platform == 'darwin': subprocess.run(['shutdown', '-r', 'now'])
                elif sys_platform == 'win32': subprocess.run(['shutdown', '/r', '/t', '0'])

            elif data == 'button-shutdown-press':
                await bot.answer_callback_query(callback_query.id, STRS.shutdown, show_alert=True)

                if sys_platform == 'linux': subprocess.run(['shutdown', 'now'])
                elif sys_platform == 'darwin': subprocess.run(['shutdown', '-h', 'now'])
                elif sys_platform == 'win32': subprocess.run(['shutdown', '/s', '/t', '0'])

    @property
    def keyboard(self) -> object:
        """ Get generated inline keyboard.

        Returns:
            object: Inline keyboard.
        """
        return self.__inline_kb


class TM_Whitelist:
    __logger = logging.getLogger("TM.Whitelist")

    @classmethod
    def is_whitelisted(cls, user_id: int) -> bool:
        """ Check is user in whitelist.

        Args:
            user_id (int): Telegram user id.

        Returns:
            bool:
                True - User is whitelisted.
                False - User is not whitelisted.
        """
        users = cls.get_whitelist()
        if user_id in users:
            return True
        else:
            return False

    @staticmethod
    def get_whitelist() -> list:
        """ Get all whitelisted users from config file.

        Returns:
            list: All whitelisted users.
        """
        return TM_Config.get()["whitelisted_users"]

    @classmethod
    async def send_to_all(cls, bot: object, message: str) -> bool:
        """ Send message to all users in whitelist.

        Args:
            bot (object): aiogram bot object.
            message (str): Text of the message.

        Returns:
            bool:
                True - Message sent.
                False - Message not sent.
        """
        for user in cls.get_whitelist():
            try:
                await bot.send_message(user, message, parse_mode=PARSE_MODE)
                return True
            except Exception as e:
                cls.__logger.error(f"Can't send message to whitelisted user [{user}]: < {e} >")
                return False


class TM_Config:
    __config = {}
    __last_mod_time = None
    __logger = logging.getLogger("TM.Config")

    def __init__(self):
        """
        Initialize configuration file.
        If the configuration file is not found - it will be created.
        If the configuration file is found - it will be checked for all necessary values.
        """
        if not self.is_exist():
            self.create()
            print(f"Config file was generated in < {PATH_CFG} >.\nFirst, you need to configure it's values and then run the script again.")
            self.__logger.info("First start detected")
            exit()
        else:
            cfg = self.get()
            up_to_date = True
            has_deprecated_values = False

            # Add not existing values
            for def_key in DEF_CFG:
                if def_key not in cfg:
                    up_to_date = False
                    cfg.update({def_key: DEF_CFG[def_key]})

            # Delete deprecated values
            for key in tuple(cfg):
                if key not in DEF_CFG:
                    has_deprecated_values = True
                    del(cfg[key])

            if not up_to_date or has_deprecated_values: self.write(cfg)

            log_message = "Config file "
            if up_to_date: log_message += "is up-to-date"
            else: log_message += "was updated with new keys"

            if has_deprecated_values: log_message += " and deprecated keys were removed"

            self.__logger.info(log_message)

    @classmethod
    def create(cls):
        """ Create config file with default values. """
        cls.write(DEF_CFG)
        cls.__logger.info("Config file was generated.")

    @staticmethod
    def write(config_dict: dict):
        """ Rewrite configuration file with new values.

        Args:
            config_dict (dict): Dictionary with new config values.
        """
        with open(PATH_CFG, 'wt') as f:
            json.dump(config_dict, f, indent=4)

    @classmethod
    def get(cls) -> dict:
        """ Get json configuration file values.

        If config file wasn't changed from last read - get values from variable,
        Else - Read values from modified file.

        Returns:
            dict: Parsed configuration json file.
        """
        if cls.is_modified():
            with open(PATH_CFG, 'rt') as f:
                cls.__config = json.load(f)
            cls.__last_mod_time = os.path.getmtime(PATH_CFG)

        return cls.__config

    @classmethod
    def is_modified(cls) -> bool:
        """ Check if config file was modified from the last load.

        Returns:
            bool:
                True - On first config request and if file was modified.
                False - File is is up-to-date with loaded values.
        """
        if cls.__last_mod_time is None:
            return True
        else:
            cfg_modtime = os.path.getmtime(PATH_CFG)
            if cfg_modtime > cls.__last_mod_time: return True
            else: return False

    @staticmethod
    def is_exist() -> bool:
        """ Check configuration file existence.

        Returns:
            bool:
                True - Config file exists.
                False - Config file doesn't exist.
        """
        return True if os.path.isfile(PATH_CFG) else False
