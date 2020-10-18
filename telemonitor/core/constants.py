from aiogram.types import ParseMode
from aiogram.utils.markdown import code


MAX_LOGS = 30
DIR_LOG = "./Logs"
PATH_CFG = "./config.json"
PATH_SHARED_DIR = "./Shared"
PARSE_MODE = ParseMode.MARKDOWN_V2
DEF_CFG = {
    "config_version": 2,
    "log_files_max": MAX_LOGS,
    "bot": {
        "token": "",
        "whitelisted_users": [],
        "state_notifications": True,
        "enable_file_transfer": True
    },
    "systemd_service": {
        "version": -1,
        "launcher_script_path": "./extensions/systemd_service/files/telemonitor_start.sh poetry"
    }
}


class STRS:
    name = "Telemonitor"
    description = "Telegram bot for monitoring your system."
    reboot = "Rebooting the system"
    shutdown = "Shutting down the system"
    message_startup = code("System was booted")
    message_shutdown = code("System is shutting down")
