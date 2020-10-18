import json
from logging import getLogger
from os import path, makedirs

from . import constants
from .cli import tm_colorama, print_action


def init_shared_dir() -> bool:
    """ Initialize dir for shared files

    Returns:
        bool:
            True - Dir doesn't exist and was created.
            False - Dir already exists.
    """
    if not path.exists(constants.PATH_SHARED_DIR):
        makedirs(constants.PATH_SHARED_DIR)
        return True
    else:
        return False


class TM_Whitelist:
    __logger = getLogger(__name__)

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
        return user_id in users

    @classmethod
    def get_whitelist(cls) -> list:
        """ Get all whitelisted users from config file.

        Returns:
            list: All whitelisted users.
        """
        from telemonitor.__main__ import args
        cls.__logger.debug('Whitelist read request')
        whitelist = TM_Config.get()["bot"]["whitelisted_users"] if args.whitelist_overwrite is None else args.whitelist_overwrite
        cls.__logger.debug(f"Whitelist content: {whitelist}")

        return whitelist

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
                await bot.send_message(user, message, parse_mode=constants.PARSE_MODE)
                cls.__logger.debug(f"Successfully sent startup message to user [{user}]")
                return True
            except Exception as e:
                cls.__logger.error(f"Can't send message to whitelisted user [{user}]: < {str(e)} >")
                return False


class TM_Config:
    __config = {}
    __last_mod_time = None
    __logger = getLogger(__name__)

    def __init__(self):
        """
        Initialize configuration file.
        If the configuration file is not found - it will be created.
        If the configuration file is found - it will be checked for all necessary values.
        """
        from telemonitor.__main__ import args

        colorama = tm_colorama()
        if not self.is_exist():
            self.create()
            self.__logger.info("First start detected")
            print(f"Config file was generated in {colorama.Fore.CYAN}{path.abspath(constants.PATH_CFG)}")

            if args.token_overwrite and args.whitelist_overwrite:
                text = "Reading bot token and whitelist from input arguments"
                self.__logger.info(text)
                print_action(text)
            else:
                # Generate config file and exit if no token and whitelist startup args provided
                print("First, you need to configure it's values and then run the script again.")
                exit()

        cfg = self.get()

        if args.disable_config_check:
            self.__logger.info('Configuration file check skipped')
        else:
            config_check_result = self.config_check(cfg)

            if not config_check_result[0] or config_check_result[1] or config_check_result[2]:
                self.write(cfg)

            log_message = "Config file "
            if config_check_result[0]:
                log_message += "is up-to-date"
            else:
                log_message += "was updated with new keys"

            if config_check_result[1]:
                log_message += " and deprecated keys were removed"

            self.__logger.info(log_message)

    @classmethod
    def create(cls):
        """ Create config file with default values. """
        cls.write(constants.DEF_CFG)
        cls.__logger.info("Config file was generated.")

    @classmethod
    def write(cls, config_dict: dict):
        """ Rewrite configuration file with new values.

        Args:
            config_dict (dict): Dictionary with new config values.
        """
        with open(constants.PATH_CFG, 'wt') as f:
            json.dump(config_dict, f, indent=4)
        cls.__logger.debug("Successful write request to configuration file")

    @classmethod
    def get(cls) -> dict:
        """ Get json configuration file values.

        If config file wasn't changed from last read - get values from variable,
        Else - Read values from modified file.

        Returns:
            dict: Parsed configuration json file.
        """
        if cls.is_modified():
            with open(constants.PATH_CFG, 'rt') as f:
                cls.__config = json.load(f)
            cls.__last_mod_time = path.getmtime(constants.PATH_CFG)

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
            cfg_modtime = path.getmtime(constants.PATH_CFG)
            return cfg_modtime > cls.__last_mod_time

    @staticmethod
    def is_exist() -> bool:
        """ Check configuration file existence.

        Returns:
            bool:
                True - Config file exists.
                False - Config file doesn't exist.
        """
        return True if path.isfile(constants.PATH_CFG) else False

    @classmethod
    def config_check(cls, config: dict) -> tuple:
        """ Configuration file recursive check system

        Args:
            config (dict): Parsed configuration file that will be modified

        Returns:
            tuple: (
                bool,  # up to date
                bool,  # has deprecated keys
                bool   # was merged to newer version
            )
        """
        def special_update_check() -> bool:
            """ Non-automatic config updater for correct merge between major config file updates

            Returns:
                bool: Was config file updated
            """
            is_updated = False

            if "config_version" not in config:
                # Update config dict to version 2
                # First version of config file doesn't have key 'config_version'
                config.update({
                    "bot": {
                        "token": config.get("api_key", ""),
                        "whitelisted_users": config.get("whitelisted_users", []),
                        "state_notifications": config.get("state_notifications", constants.DEF_CFG["bot"]["state_notifications"]),
                        "enable_file_transfer": config.get("enable_file_transfer", constants.DEF_CFG["bot"]["enable_file_transfer"])
                    }
                })
                is_updated = True
                cls.__logger.info("Successfully merged config file to version 2")

            return is_updated

        def add_new_keys(default_config=constants.DEF_CFG, user_config=config) -> bool:
            up_to_date = True

            for k, v in list(default_config.items()):
                if type(v) == dict:
                    if k not in user_config:
                        user_config[k] = v
                        up_to_date = False
                    else:
                        up_to_date = add_new_keys(v, user_config[k])
                elif k not in user_config:
                    up_to_date = False
                    user_config.update({k: v})
                    cls.__logger.debug(f"Adding new key '{k}' to user configuration file")

            return up_to_date

        def remove_deprecated(default_config=constants.DEF_CFG, user_config=config) -> bool:
            has_deprecated_values = False

            for k, v in list(user_config.items()):
                if type(v) == dict:
                    has_deprecated_values = remove_deprecated(default_config[k], v)
                elif k not in default_config:
                    has_deprecated_values = True
                    del(user_config[k])
                    cls.__logger.debug(f"Removing deprecated key '{k}' from user configuration file")

            return has_deprecated_values

        # Prepare output in right order
        special_check = special_update_check()
        any_deprecated = remove_deprecated()
        any_new = add_new_keys()

        return (
            any_new,
            any_deprecated,
            special_check
        )
