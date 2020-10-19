import os
import logging
from time import strftime, asctime

from .. import __version__
from .io import TM_Config, create_dirs_on_path
from .constants import DIR_LOG, MAX_LOGS, STRS
from .cli import tm_colorama, print_action


def init_logger(is_verbose: bool = False):
    """ Initialize python `logging` module

    Args:
        is_verbose (bool, optional): Write more detailed information to log file. Defaults to False.
    """
    colorama = tm_colorama()

    if not create_dirs_on_path(DIR_LOG, True):
        log_files = [f for f in os.listdir(DIR_LOG) if os.path.isfile(os.path.join(DIR_LOG, f))]
        log_files_len = len(log_files)
        if log_files_len > (TM_Config.read().get("log_files_max", MAX_LOGS) if TM_Config.is_exist() else MAX_LOGS):
            print_action(f"Clearing logs folder. {colorama.Fore.RED}{log_files_len}{colorama.Fore.RESET} files will be removed")
            for log_file in log_files:
                os.remove(os.path.join(DIR_LOG, log_file))

    log_level = logging.DEBUG if is_verbose else logging.INFO
    filename = f'{DIR_LOG}/TMLog_{strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=filename, format="[%(asctime)s][%(levelname)s][%(name)s->%(funcName)s]: %(message)s", level=log_level)

    with open(filename, 'wt') as f:
        f.write(f"{STRS.name} ({__version__}) : [ {asctime()} ]\n\n")
