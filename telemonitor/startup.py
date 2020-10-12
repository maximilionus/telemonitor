import logging
from os import chdir, path

from colorama import init as colorama_prepare

from telemonitor import core
from telemonitor.extensions import systemd_service
from telemonitor.bot import start_telegram_bot


def run():
    from telemonitor.__main__ import args

    colorama_prepare(autoreset=True)
    chdir(path.dirname(__file__))

    if not args.disable_logging:
        core.init_logger(args.verbose)
    else:
        core.print_action("Starting without logging module initialization")

    logger = logging.getLogger(__name__)
    logger.info("Telemonitor is starting")

    # Initialize config
    core.TM_Config()
    if args.config_check_only: exit()

    if args.systemd_service is not None:
        systemd_service.cli(args.systemd_service)

    start_telegram_bot()
