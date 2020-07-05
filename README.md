# Telemonitor
- [Telemonitor](#telemonitor)
  - [Main Information](#main-information)
  - [Features](#features)
    - [Stable](#stable)
    - [Development](#development)
  - [How to run](#how-to-run)
  - [Bot Commands](#bot-commands)
  - [Optional Arguments](#optional-arguments)
  - [File Transfer System *(FTS)*](#file-transfer-system-fts)
    - [How to use](#how-to-use)
  - [Configuration File](#configuration-file)
    - [Default Config](#default-config)
  - [Supported Platforms](#supported-platforms)
  - [Logging](#logging)


## Main Information
Telemonitor is a telegram bot based on [aiogram](https://github.com/aiogram/aiogram) for system monitoring. Bot is currently in progress of development, so new features will probably be `added`/`changed`/`deprecated`.


## Features
### Stable

- Show system information (OS, Architecture, Uptime, User@Host)
- Reboot or Shutdown the system
- Notification message to all *whitelisted users* on bot startup
- [File transfer system](#file-transfer-system) *(Currently works only as `file`/`image` receiver)*
- Modify whitelisted users without restart

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
| Arg            | Description                                 |
| :------------- | :------------------------------------------ |
| `-h`, `--help` | Show help message and exit                  |
| `--verbose`    | Write more detailed information to log file |
| `--dev`        | Enable unstable development features        |


## File Transfer System *(FTS)*
This feature allows you to transfer files between bot's host machine and telegram user. Feature can be disabled by setting value of key `enable_file_transfer` to `false` in [configuration file](#configuration-file). All downloaded files will be saved to `./Telemonitor/Shared` directory *(Does not exist by default and will be created on first `FTS` call)*.

> Note that **all transfered files will be stored on Telegram servers!**

> Currently this system supports only `documents` and `images` transfer **only from** *whitelisted telegram user* to *bot's host machine*

### How to use
- Simply send any `file`/`image` to bot from your client and you will receive notification when all files will be downloaded to host.


## Configuration File
This configuration file will be generated on first start in `./Telemonitor/` directory and needs to be modified.

Configuration file will be automatically checked on each bot start to remove deprecated and add new *keys*. All actions with config file will be listed in [log file](#logging).

### Default Config
```jsonc
{
    "api_key": "123:token__here", // Telegram bot api token
    "whitelisted_users": [12345, 54321, 224414], // Array with all whitelisted users ids
    "state_notifications": true, // Enable/Disable notification message on boot and shutdown event
    "enable_file_transfer": true // Enable/Disable file transfer system
}
```


## Supported Platforms
All list of features and supported platforms.

| Platform →<br>Feature ↓ | Linux | Windows | macOS |
| :---------------------- | :---- | :------ | :---- |
| `System Information`    | ✓     | ✓       | ⍻     |
| `Shutdown` & `Reboot`   | ✓     | ✓       | ⍻     |
| `Uptime`                | ✓     | ✓       | ⍻     |
| `File Transfer System`  | ✓     | ✓       | ⍻     |

> *Legend*  
> `✓` - Available  
> `⍻` - Available but not tested  
> `✗` - Not available


## Logging
**Telemonitor** also supports logging with python [`logging`](https://docs.python.org/3/library/logging.html) module. All logs will be saved to `./Telemonitor/Logs/` in format: `TMLog_YYYY-MM-DD_HH-MM-SS.log`