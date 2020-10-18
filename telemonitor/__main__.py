from .core.cli import cli_arguments_parser
from . import startup


args = cli_arguments_parser()


def run():
    startup.run()


if __name__ == "__main__":
    run()
