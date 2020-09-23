# Telemonitor Changelog

[Development](https://github.com/maximilionus/Telemonitor/tree/development)
- Changed logging formatting to display exact used module and function names


[**2.0.0**](https://github.com/maximilionus/Telemonitor/releases/tag/v2.0.0)
> This major update is focused on fixing `linux`-related issues, but due to backward incompatible changes in code, this release will be marked as **major**.
- Renamed project package name from `Telemonitor` to `telemonitor`
- Problem with project package installation on `linux` systems was solved.

[**1.1.1**](https://github.com/maximilionus/Telemonitor/releases/tag/v1.1.1)
- Fixed version of package

[**1.1.0**](https://github.com/maximilionus/Telemonitor/releases/tag/v1.1.0)
- Added `setup.py` script for project package installation instead of force scanning with `pyproject.toml` *(This will also fix the issue with linux project installation)*
- Changed path info of configuration file on first start from *relative* to *absolete*
- Changed minimal version of `python` to `>= 3.7` *(was `^3.8`)*

[**1.0.0**](https://github.com/maximilionus/Telemonitor/releases/tag/v1.0.0)
> Configuration file from previous versions **will work** with this major update. There's no need to remove it.
- Implemented [file transfer system](./README.md#file-transfer-system-fts). Currently works only as `file`/`image` receiver.
- Reply with *alert* message to `Shutdown` and `Reboot` buttons press
- Start menu:
  - Added information about system version to *Sys Info* button reply
  - Enhanced *uptime* output. Was: `0:21:2:34`, Now: `00:21:02:32`
- Added `config file` values scan on bot startup
  - Add new values
  - Remove deprecated
- Maximum log files number now can be configured
- Added simple unit test for script version match
- Added arguments handling (with `argparse` module)
  - Added arg `--verbose` : Write more detailed information to log file
  - Added arg `--dev` : Enable unstable development features
- Added bot version to logging
- Added new params to `config.json` ([Read about their meaning here](./README.md#configuration-file "Readme file link")):
  - `"log_files_max"`
  - `"state_notifications"`
  - `"enable_file_transfer"`
- *On shutdown* notification message was moved to [development features](./README.md#development)
- Changed [`TM_ControlInlineKB`](./Telemonitor/helpers.py) class method `get_keyboard()` to *@property* `keyboard` and made all class variables *private*
- `STRS` in [helpers.py](./Telemonitor/helpers.py) was turned into a *class* instead of *dict*
- Default logging level changed to `INFO`
- Enhanced already imported modules usage

[**0.2.5**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.2.5)
- Added automatic logs cleanup after exceeding the log files limit. Look for const `MAX_LOGS` in [`helpers.py`](./Telemonitor/helpers.py)
- Added configuration file loading optimization (Read config file values only if this file was modified)
- Remove version information from `/start` command reply. Version is now shows in console on script boot.

[**0.1.5**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.1.5)
- Full switch to [semantic versioning](https://semver.org/)
- Added `macOS` support for `Shutdown` and `Reboot` commands
- Changed main Inline Keyboard buttons position
- Changed `/start` command reply message a little bit
- Enhanced logging

[**0.0.5**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.5) : 2020-06-29
- Added text for `reboot` and `shutdown` buttons callback instead of message reply
- Added message on bot exit
- Unified send to whitelisted users function in TM_Whitelist

[**0.0.4**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.4) : 2020-06-28
- Added on-start bot message to all whitelisted users.

[**0.0.3**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.3) : 2020-06-28
- **Sys Info** button message: Move `Architecture` to `System`
- Pack all `TM_ControlInlineKB` buttons into enum
- Poetry run command is now `telem` *(was: `telemonitor-start`)*
- Fixed paths handling. File read/write now in script's dir
- On-start notification message to stdout

[**0.0.2**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.2) : 2020-06-26
- Added whitelist check for buttons callback handler
- Added support for easy `poetry run ...` command
- Whitelisted check function update

[**0.0.1**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.1) : 2020-06-26
- Bot functionality done
- Added whitelist
- Added configuration file r/w
