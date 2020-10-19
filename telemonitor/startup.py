import logging
from os import chdir, path

import colorama

from .core.io import TM_Config
from .core.cli import print_action, handle_startup_args
from .bot import start_telegram_bot
from .core.logging import init_logger


def run():
    from telemonitor.__main__ import args

    colorama.init(autoreset=True)
    chdir(path.dirname(__file__))

    if not args.disable_logging:
        init_logger(args.verbose)
    else:
        print_action("Starting without logging module initialization")

    logger = logging.getLogger(__name__)
    logger.info("Telemonitor is starting")

    # Initialize config
    TM_Config()

    handle_startup_args(args)

    start_telegram_bot()
