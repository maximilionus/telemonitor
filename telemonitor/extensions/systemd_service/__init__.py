from sys import platform
from logging import getLogger
from os import path, remove
from typing import Tuple, List

from telemonitor.core import TM_Config, DEF_CFG, tm_colorama, print_action


__version_service_file = 2
__logger = getLogger(__name__)

# All relative paths are starting from root directory of module `telemonitor`,
# Not from this directory!
__service_config_template_path = './extensions/systemd_service/files/telemonitor-bot-template.service'
__service_config_final_path = '/lib/systemd/system/telemonitor-bot.service'


def cli(mode: str):
    colorama = tm_colorama()
    __shell_launch_script_path = TM_Config.get()["systemd_service"]["launcher_script_path"]

    if platform == 'linux':
        if mode == 'install':
            if service_install():
                print("Successfully installed Telemonitor systemd service to your linux system!",
                      "\n- Service",
                      f"\n\tName: {colorama.Fore.CYAN}{path.basename(__service_config_final_path)}{colorama.Fore.RESET}",
                      f"\n\tPath: {colorama.Fore.CYAN}{__service_config_final_path}{colorama.Fore.RESET}",
                      f"\n\tVersion: {colorama.Fore.CYAN}{__version_service_file}{colorama.Fore.RESET}",
                      "\n\nNow, the only thing you need to do is to run this command to detect a new service:",
                      f"\n\t{colorama.Fore.GREEN}systemctl daemon-reload{colorama.Fore.RESET}",
                      "\n\nAnd now you can manually control this service with:",
                      f"\n\t{colorama.Fore.GREEN}systemctl status {path.basename(__service_config_final_path)}{colorama.Fore.RESET}  # View Telemonitor logs and current status",
                      f"\n\t{colorama.Fore.GREEN}systemctl start {path.basename(__service_config_final_path)}{colorama.Fore.RESET}   # Start the Telemonitor service",
                      f"\n\t{colorama.Fore.GREEN}systemctl stop {path.basename(__service_config_final_path)}{colorama.Fore.RESET}    # Stop the Telemonitor service"
                      f"\n\t{colorama.Fore.GREEN}systemctl enable {path.basename(__service_config_final_path)}{colorama.Fore.RESET}  # Start Telemonitor service on system launch"
                      f"\n\t{colorama.Fore.GREEN}systemctl disable {path.basename(__service_config_final_path)}{colorama.Fore.RESET} # Disable Telemonitor service automatic startup",
                      "\n\nPlease note, that the commands above will require root user privileges to run."
                      )
            else:
                print("Telemonitor systemd service is already installed on this system")

        elif mode == 'upgrade':
            if not service_upgrade():
                print(f"Service file is up-to-date. Current version is: {colorama.Fore.CYAN}{__version_service_file}")

        elif mode == 'remove':
            if service_remove():
                print("Successfully removed service from system")
            else:
                print("Systemd service configuration file doesn't exist, nothing to remove")

        elif mode == 'status':
            cfg_service = TM_Config.get()['systemd_service']
            service_exists = __systemd_config_exists()
            text = f"Telemonitor Systemd Service - Status\
                     \n\n- Is installed: {colorama.Fore.CYAN}{service_exists}{colorama.Fore.RESET}"

            if service_exists:
                text += f"\n- Version : {colorama.Fore.CYAN}{cfg_service['version']}{colorama.Fore.RESET}\
                          \n- Service path : {colorama.Fore.CYAN}{__service_config_final_path}{colorama.Fore.RESET}\
                          \n- Startup script path : {colorama.Fore.CYAN}{path.abspath(__shell_launch_script_path)}{colorama.Fore.RESET}"
            print(text)

        elif mode == 'apply':
            result = service_apply_changes()

            if result[0] == 1:
                text = "Successfully merged this changes to service file:"

                for merged_item in result[1]:
                    text += f"\n- {colorama.Fore.CYAN}{merged_item}{colorama.Fore.RESET}"

                print(text)

            elif result[0] == 2:
                print("Nothing to merge, service file is up-to-date")
            elif result[0] == 0:
                print("Service is not installed, can't apply changes")

    else:
        print(f"This feature is available only for {colorama.Fore.CYAN}linux{colorama.Fore.RESET} platform with systemd support.\nYour platform is {colorama.Fore.CYAN}{platform}{colorama.Fore.RESET}.")
        __logger.error(f"Requested feature is available only on 'linux' platforms with systemd support. Your platform is {platform}")

    exit()


def service_install() -> bool:
    """ Install systemd service

    Returns:
        bool: Was service installed
    """
    __logger.info("Begin systemd service installation")
    __shell_launch_script_path = TM_Config.get()["systemd_service"]["launcher_script_path"]
    colorama = tm_colorama()
    result = False

    if not __systemd_config_exists():
        try:
            template_service_file = open(__service_config_template_path, 'rt')
            final_service_file = open(__service_config_final_path, 'wt')

            text = template_service_file.read()
            text = text.replace('<SHELL_SCRIPT_PATH>', path.abspath(__shell_launch_script_path))

            final_service_file.write(text)
        except Exception as e:
            e_text = f"Can't write systemd service config file to {__service_config_final_path} due to {str(e)}"
            print(f"{colorama.Fore.RED}{e_text}\n")
            __logger.error(e_text)
            exit()
        else:
            __update_cfg_values('install')
            __logger.info("Systemd service was successfully installed on system.")
            template_service_file.close()
            final_service_file.close()
            result = True

    else:
        __logger.error(f"Service file already exists in '{__service_config_final_path}'")

    return result


def service_upgrade() -> bool:
    """ Check systemd service config files and upgrade them to newer version if available

    Returns:
        bool: Was service updated
    """
    was_updated = False
    colorama = tm_colorama()
    __logger.info("Begin systemd service upgrade check")

    if __systemd_config_exists():
        config = TM_Config.get()

        builtin_version = __version_service_file
        installed_version = config["systemd_service"]["version"]

        if installed_version < builtin_version:
            choice = input(f"Service file can be upgraded to version {colorama.Fore.CYAN}{builtin_version}{colorama.Fore.RESET} (Current version: {colorama.Fore.CYAN}{installed_version}{colorama.Fore.RESET}). Upgrade? {colorama.Fore.GREEN}[y/n]{colorama.Fore.RESET}: ")
            if choice[0].lower() == 'y':
                print_action(f"Removing installed version {colorama.Fore.CYAN}{installed_version}{colorama.Fore.RESET} service from system...", start="\n")
                if service_remove():
                    print_action(
                        "Installed version of service was removed",
                        f"Installing the systemd service version {colorama.Fore.CYAN}{builtin_version}{colorama.Fore.RESET} to system..."
                    )
                    if service_install():
                        print_action("Successfully installed new systemd service")
                        __update_cfg_values('upgrade')
                        print(f"\nService was successfully upgraded from version {colorama.Fore.CYAN}{installed_version}{colorama.Fore.RESET} to {colorama.Fore.CYAN}{builtin_version}{colorama.Fore.RESET}")
                        was_updated = True
    else:
        text = "Service is not installed, nothing to upgrade"
        __logger.info(text)
        print(text)

    return was_updated


def service_remove() -> bool:
    """ Remove all systemd service files, generated by Telemonitor, from system

    Returns:
        bool:
            True - Successfully removed service from system
            False - Can't remove service
    """
    __logger.info("Begin systemd service removal")
    result = False
    colorama = tm_colorama()

    if __systemd_config_exists():
        try:
            remove(__service_config_final_path)
        except Exception as e:
            print(f"Can't remove systemd service file in {colorama.Fore.CYAN}{__service_config_final_path}{colorama.Fore.RESET} due to {colorama.Fore.RED}{str(e)}")
            __logger.error(f"Can't remove systemd service file in {__service_config_final_path} due to {str(e)}")
        else:
            __update_cfg_values('remove')
            __logger.info(f"Successfully removed service file on path {__service_config_final_path}")
            result = True
    else:
        __logger.error("Systemd service configuration file doesn't exist, nothing to remove")

    return result


def service_apply_changes() -> Tuple[int, List[str]]:
    """ Merge all changes from configuration file to systemd service file

    Returns:
        int:
            0 - Service is not installed
            1 - Successfully merged configuration file values to service file
            2 - No changes to merge, up-to-date
        list[str]: What was merged to service file
    """
    __logger.info("Begin service changes merging procedure")
    result_int = 0
    result_list = []

    if __systemd_config_exists():
        with open(__service_config_final_path, 'r+') as service_file:
            service_text = service_file.readlines()

            for line in service_text:
                if "ExecStart=" in line:
                    # Apply changes for launch script path
                    launch_script_path_read = line.split('=')[1][:-1]
                    launch_script_path_config = path.abspath(TM_Config.get()["systemd_service"]["launcher_script_path"])
                    __logger.debug(f"Begin 'ExecStart' param check. Service file value: {launch_script_path_read}, Config file value: {launch_script_path_config}")

                    if launch_script_path_read != launch_script_path_config:
                        service_text[service_text.index(line)] = f"\tExecStart={launch_script_path_config}\n"
                        result_int = 1
                        result_list.append("Launcher script path")

                    else:
                        result_int = 2

            if result_int == 1:
                service_file.truncate(0)
                service_file.seek(0)
                service_file.writelines(service_text)
                __logger.info("Successfully merged all changes from configuration file to service file")
                __logger.debug(f"List of changes: {result_list}")

            elif result_int == 2:
                __logger.info("Service file is already up-to-date")
    else:
        __logger.info("Service is not installed, nothing to apply")

    return (result_int, result_list)


def __systemd_config_exists() -> bool:
    """ Check for systemd config existence

    Returns:
        bool:
            True - Config exists
            False - Can't find any config file
    """
    return path.isfile(__service_config_final_path)


def __update_cfg_values(mode: str):
    """ Update config values related to systemd service

    Args:
        mode (str):
            'install' - Set config values to fresh install version.
            'upgrade' - Upgrade value of `version` key in config.
            'remove' - Reset `systemd_service` dict to default values.
    """
    options = ('install', 'upgrade', 'remove')
    if mode not in options:
        raise Exception(f"Option '{mode}' doesn't exist in this function")

    cfg = TM_Config.get()

    if mode == 'install':
        cfg['systemd_service']["version"] = __version_service_file
    elif mode == 'upgrade':
        cfg['systemd_service']["version"] = __version_service_file
    elif mode == 'remove':
        cfg['systemd_service']['version'] = DEF_CFG['systemd_service']['version']

    TM_Config.write(cfg)
    __logger.debug(f"Updated configuration dict 'systemd_service' to mode '{mode}'")
