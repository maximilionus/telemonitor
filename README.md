# Telemonitor
- [Telemonitor](#telemonitor)
  - [Main Information](#main-information)
  - [Functionality](#functionality)
  - [How to run](#how-to-run)
  - [Commands](#commands)
  - [Configuration File](#configuration-file)

## Main Information
Telemonitor is a telegram bot based on [aiogram](https://github.com/aiogram/aiogram) for system monitoring.

## Functionality
- Show system information (OS, Architecture, Uptime, User@Host).
- Reboot or Shutdown the system.

> Bot is currently in progress of development, so new features will probably be added.

## How to run
> Note that bot requires access to some system commands *(such as `shutdown` and `reboot`)*, so if you want all features to work as intended - run all commands from `root` *(with `sudo`)* or from user who has full access to those commands.
1. Install [`poetry`](https://github.com/python-poetry/poetry) dependency manager with `pip` or [from source](https://github.com/python-poetry/poetry#installation).
2. Go to cloned `Telemonitor` repository folder and run:
   ```bash
   poetry install --no-dev
   ```
3. Go to `./Telemonitor/`
4. After all packages successfully installed, run:
   ```bash
   poetry run telemonitor-start
   ```
5. On the first start `Telemonitor` will generate `config.json` *([About Config](#configuration-file))* file in current dir and exit. You will have to add `bot token` and `whitelisted users` to `config.json` and then go to `3.`

## Commands
```
start - Start the bot
```

## Configuration File
> This configuration file will be generated on first start in `./Telemonitor/` and needs to be modified.
```jsonc
{
    "api_key": "123:token__here", // Telegram bot api token
    "whitelisted_users": [12345, 54321, 224414] // Array with all whitelisted users ids
}
```