import logging
from os import chdir, path

import colorama

from .core.io import TM_Config
from .core.cli import print_action
from .bot import start_telegram_bot
from .core.logging import init_logger
from .extensions import systemd_service


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
    if args.config_check_only: exit()

    if hasattr(args, 'service_cli_command'):
        systemd_service.cli(args.service_cli_command)

    start_telegram_bot()
