# Telemonitor
- [Telemonitor](#telemonitor)
  - [Main Information](#main-information)
  - [Features](#features)
    - [Stable](#stable)
    - [Development](#development)
  - [How to run](#how-to-run)
  - [Bot Commands](#bot-commands)
  - [Optional Arguments](#optional-arguments)
  - [Configuration File](#configuration-file)
    - [Default Config](#default-config)
  - [File Transfer System *(FTS)*](#file-transfer-system-fts)
    - [How to](#how-to)
  - [Systemd Service Control](#systemd-service-control)
    - [How to](#how-to-1)
  - [Supported Platforms](#supported-platforms)
  - [Logging](#logging)


## Main Information
Telemonitor is a telegram bot based on [aiogram](https://github.com/aiogram/aiogram) for system monitoring. Bot is currently in progress of development, so features can be `added`/`changed`/`deprecated`.


## Features
### Stable

- Show system information (OS, Architecture, Uptime, User@Host)
- Reboot or Shutdown the system
- Notification message to all *whitelisted users* on bot startup
- [File transfer system](#file-transfer-system) *(Currently works only as `file`/`image` receiver)*
- Modify whitelisted users without restart
- Support of automated systemd service generation on linux machines (See [Systemd Service Control](#systemd-service-control))

### Development
Development features are in progress of development and *are unstable*, so they're disabled by default. Enable with [argument `--dev`](#optional-arguments). Use at your own risk and be ready to drown in errors.

- Send notification message to all whitelisted users on shutdown


## How to run
> Note that bot requires access to some system commands *(such as `shutdown` and `reboot`)*, so if you want all features to work as intended - run all commands from `root` *(with `sudo`)* or from user who has full access to those commands.
1. Install [`poetry`](https://github.com/python-poetry/poetry) dependency manager with `pip` or [from source](https://github.com/python-poetry/poetry#installation).
2. Go to cloned `Telemonitor` repository folder and run:
   ```bash
   poetry install --no-dev
   ```
3. After all packages successfully installed, run:
   ```bash
   poetry run telem
   ```
4. On the first start `Telemonitor` will generate `config.json` *([about config](#configuration-file))* and exit. You will have to add `bot token` and `whitelisted users` to `config.json` and then go to `3.`


## Bot Commands
```
start - Start the bot
```


## Optional Arguments
| Arg                                               | Description                                                                              |
| :------------------------------------------------ | :--------------------------------------------------------------------------------------- |
| `-h`, `--help`                                    | show help message and exit                                                               |
| `--version`                                       | show program's version number and exit                                                   |
| `--no-color`                                      | disable colored output (ANSI escape sequences)                                           |
| `--token` STR                                     | force the bot to run with token from the argument instead of the configuration file      |
| `--whitelist` INT [INT ...]                       | force the bot to check whitelisted users from argument instead of the configuration file |
| `--systemd-service` install/upgrade/remove/status | automated systemd service control for `linux` platforms                                  |
| `--dev`                                           | enable unstable development features                                                     |
| `--verbose`, `-v`                                 | write debug information to log file                                                      |
| `--config-check`                                  | run config file initialization procedure and exit                                        |
| `--no-config-check`                               | don't scan configuration file on start                                                   |


## Configuration File
This configuration file will be generated on first start in `./telemonitor/` directory and needs to be modified.

Configuration file will be automatically checked on each bot start to remove deprecated and add new *keys*, so there's *no need* to remove it on each update. All actions with config file will be listed in [log file](#logging).

### Default Config
```jsonc
{
    "config_version": 2,            // Version of configuration file. Used for correct keys migration on update
    "log_files_max": 30,            // Maximum amount of .log files in logs directory
    "bot": {
        "token": "123:token__here", // Telegram bot api token
        "whitelisted_users": [      // Array with all whitelisted users ids
            000000000,              // Sample ids
            111111111
        ],
        "state_notifications": true, // Enable/Disable notification message on boot and shutdown event
        "enable_file_transfer": true // Enable/Disable file transfer system
    },
    "systemd_service": {             // Dictionary for linux systemd service status
        "version": -1                // Version of installed service file
    }
}

```


## File Transfer System *(FTS)*
This feature allows you to transfer files between bot's host machine and telegram user. Feature can be disabled by setting value of key `enable_file_transfer` to `false` in [configuration file](#configuration-file). All downloaded files will be saved to `./Telemonitor/Shared` directory *(Does not exist by default and will be created on first `FTS` call)*.

> Note that **all transfered files will be stored on Telegram servers!**

> Currently this system supports only `documents` and `images` transfer **only from** *whitelisted telegram user* to *bot's host machine*

### How to
- Simply send any `file`/`image` to bot from your client and you will receive notification when all files will be downloaded to host.


## Systemd Service Control
There's speical feature available **only** for `linux` platforms with `systemd` software suite. It provides user-friendly CLI to control *(install, remove, upgrade)* **systemd service**.

### How to
> Please note that you must run Telemonitor as root to install the service correctly.

> You will get output with the result of all CLI commands to your terminal and [log file](#logging)

- Installation of service is pretty easy. You should just run
  ```bash
  poetry run telem --systemd-service install
  ```
- To uninstall the service, run:
  ```bash
  poetry run telem --systemd-service remove
  ```
- Getting service status *(like service version)* can be done this way
  ```bash
  poetry run telem --systemd-service status
  ```
  > Note that this CLI command does not display service detailed information. To get this one you should use system command `systemctl status service-name-here`
- Checking installed service for any available upgrade
  ```bash
  poetry run telem --systemd-service upgrade
  ```
  > If any updates are available, you will be prompted to confirm their installation.


## Supported Platforms
All list of features and supported platforms.

| Platform →<br>Feature ↓     | Linux | Windows | macOS |
| :-------------------------- | :---- | :------ | :---- |
| `System Information`        | ✓     | ✓       | ⍻     |
| `Shutdown` & `Reboot`       | ✓     | ✓       | ⍻     |
| `Uptime`                    | ✓     | ✓       | ⍻     |
| `File Transfer System`      | ✓     | ✓       | ⍻     |
| `Automated Systemd Service` | ✓     | ✗       | ✗     |

> *Legend :*  
> `✓` - Available  
> `⍻` - Available, but not tested  
> `✗` - Not available


## Logging
**Telemonitor** also supports logging with python [`logging`](https://docs.python.org/3/library/logging.html) module. All logs will be saved to `./Telemonitor/Logs/` in format: `TMLog_YYYY-MM-DD_HH-MM-SS.log`. Log folder will also be automatically cleaned after exceeding log files limit *(30 files)* inside of it. This limit can be changed in [configuration file](#configuration-file).
