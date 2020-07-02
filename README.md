# Telemonitor
- [Telemonitor](#telemonitor)
  - [Main Information](#main-information)
  - [Features](#features)
  - [How to run](#how-to-run)
  - [Bot Commands](#bot-commands)
  - [Configuration File](#configuration-file)
  - [Supported Platforms](#supported-platforms)
  - [Logging](#logging)

## Main Information
Telemonitor is a telegram bot based on [aiogram](https://github.com/aiogram/aiogram) for system monitoring. Bot is currently in progress of development, so new features will probably be `added`/`changed`/`deprecated`.

## Features
- Show system information (OS, Architecture, Uptime, User@Host)
- Reboot or Shutdown the system
- Modify whitelisted users without restart

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
4. On the first start `Telemonitor` will generate `config.json` *([about Config](#configuration-file))* and exit. You will have to add `bot token` and `whitelisted users` to `config.json` and then go to `3.`

## Bot Commands
```
start - Start the bot
```

## Configuration File
This configuration file will be generated on first start in `./Telemonitor/` directory and needs to be modified.

```jsonc
{
    "api_key": "123:token__here", // Telegram bot api token
    "whitelisted_users": [12345, 54321, 224414] // Array with all whitelisted users ids
}
```

## Supported Platforms
All list of features and supported platforms.

| Platform →<br>Feature ↓ | Linux | Windows | macOS |
| :---------------------- | :---- | :------ | :---- |
| `System Information`    | ✓     | ✓       | ⍻     |
| `Shutdown` & `Reboot`   | ✓     | ✓       | ⍻     |
| `Uptime`                | ✓     | ✓       | ⍻     |

> *Legend*  
> `✓` - Available  
> `⍻` - Available but not tested  
> `✗` - Not available

## Logging
**Telemonitor** also supports logging with python `logging` module. All logs will be saved to `./Telemonitor/Logs/` in format: `TMLog_YYYY-MM-DD_HH-MM-SS.log`