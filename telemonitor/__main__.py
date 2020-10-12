from telemonitor.core import cli_arguments_parser
from telemonitor import startup


args = cli_arguments_parser()


def run():
    startup.run()


if __name__ == "__main__":
    run()
