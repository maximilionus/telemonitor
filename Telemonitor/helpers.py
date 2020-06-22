import os
from sys import exit
import logging
import json
from time import strftime
from aiogram import types as aiogram_types

DIR_LOG = os.path.abspath("./Logs")
PATH_CFG = os.path.abspath("./config.json")
DEF_CFG = {
    "api_key": "",
    "whitelisted_users": []
}


def init_logger():
    if not os.path.isdir(DIR_LOG):
        os.makedirs(DIR_LOG)
    filename = f'{DIR_LOG}/TMLog_{strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=filename, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")


class TM_Whitelist:
    def __init__(self):
        self.users = TM_Config.get()["whitelisted_users"]

    def is_whitelisted(self, message: aiogram_types.Message):
        if message.from_user.id in self.users:
            return True
        else:
            return False


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
