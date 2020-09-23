__version__ = "1"
__service_file_template_path = './telemonitor-bot-template.service'


def start(mode: str):
    if mode == 'install': install()
    elif mode == 'upgrade': upgrade()
    else: remove()


def install():
    pass


def upgrade():
    pass


def remove():
    pass


def __generate_service_file():
    pass
