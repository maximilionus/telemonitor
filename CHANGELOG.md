# Telemonitor Changelog

- [Stable Releases](#stable-releases)
- [Development Releases](#development-releases)


# Stable Releases


## [**3.0.1**](https://github.com/maximilionus/Telemonitor/releases/tag/v3.0.1) (2020-10-04)

### Fixed
- Fixed configuration file check new keys insertion issue


## [**3.0.0**](https://github.com/maximilionus/Telemonitor/releases/tag/v3.0.0) (2020-10-04)
> This major update is focused on improving `CLI` usage, features targeting the `Linux` platform and enhancing core structure with backward incompatible changes

> Configuration file from versions `^1.0.0` and `^2.0.0` will be merged to major version `^3.0.0` without any problems

### Added
- Automated systemd service creation for linux platforms implemented
- Added colored output for CLI output to enhance readability
- Overwrite *bot token* and *whitelisted users* with optional startup args `--token` and `--whitelist`
- Added new optional startup arguments *(See [README](./README.md#optional-arguments) for info)*:
  - `--version`
  - `--token`
  - `--whitelist`
  - `--systemd-service`
  - `--config-check`
  - `--no-config-check`
  - `--no-color`

### Changed
- Configuration file structure update to version `2` *(Automatic merge from version 1 is implemented too)*
  - Moved all bot related keys to `"bot": {}`
  - Renamed `"api_key"` to `"token"`
  - Added `"systemd_service"` key for systemd service params
- Enhanced configuration file scanning procedure *(for detection of deprecated and new, not added, keys)*
- Changed logging formatting to display exact used module and function names and show application name and version only on first line of log file
- Split startup arguments to groups


## [**2.0.0**](https://github.com/maximilionus/Telemonitor/releases/tag/v2.0.0) (2020-09-05)
> This major update is focused on fixing `linux`-related issues, but due to backward incompatible changes in code, this release will be marked as **major**.

### Fixed
- Problem with project package installation on `linux` systems was solved.

### Changed
- Renamed project package name from `Telemonitor` to `telemonitor`


## [**1.1.1**](https://github.com/maximilionus/Telemonitor/releases/tag/v1.1.1) (2020-09-03)

### Fixed
- Fixed version of package


## [**1.1.0**](https://github.com/maximilionus/Telemonitor/releases/tag/v1.1.0) (2020-09-02)

### Added
- Added `setup.py` script for project package installation instead of force scanning with `pyproject.toml` *(This will also fix the issue with linux project installation)*

### Changed
- Changed path info of configuration file on first start from *relative* to *absolete*
- Changed minimal version of `python` to `>= 3.7` *(was `^3.8`)*


## [**1.0.0**](https://github.com/maximilionus/Telemonitor/releases/tag/v1.0.0) (2020-07-08)

### Added
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

### Changed
- *On shutdown* notification message was moved to [development features](./README.md#development)
- Changed [`TM_ControlInlineKB`](./Telemonitor/helpers.py) class method `get_keyboard()` to *@property* `keyboard` and made all class variables *private*
- `STRS` in [helpers.py](./Telemonitor/helpers.py) was turned into a *class* instead of *dict*
- Default logging level changed to `INFO`
- Enhanced already imported modules usage


## [**0.2.5**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.2.5) (2020-07-02)

### Added
- Added automatic logs cleanup after exceeding the log files limit. Look for const `MAX_LOGS` in [`helpers.py`](./Telemonitor/helpers.py)
- Added configuration file loading optimization (Read config file values only if this file was modified)

### Removed
- Remove version information from `/start` command reply. Version is now shows in console on script boot.

## [**0.1.5**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.1.5) (2020-07-01)

### Added
- Added `macOS` support for `Shutdown` and `Reboot` commands

### Changed
- Full switch to [semantic versioning](https://semver.org/)
- Changed main Inline Keyboard buttons position
- Changed `/start` command reply message a little bit
- Enhanced logging

## [**0.0.5**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.5) (2020-06-29)

### Added
- Added text for `reboot` and `shutdown` buttons callback instead of message reply
- Added message on bot exit
- Unified send to whitelisted users function in TM_Whitelist

## [**0.0.4**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.4) (2020-06-28)

### Added
- Added on-start bot message to all whitelisted users.

## [**0.0.3**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.3) (2020-06-28)

### Added
- On-start notification message to stdout

### Changed
- **Sys Info** button message: Move `Architecture` to `System`
- Pack all `TM_ControlInlineKB` buttons into enum
- Poetry run command is now `telem` *(was: `telemonitor-start`)*
- Fixed paths handling. File read/write now in script's dir

## [**0.0.2**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.2) (2020-06-26)

### Added
- Added whitelist check for buttons callback handler
- Added support for easy `poetry run ...` command

### Changed
- Whitelisted check function update

## [**0.0.1**](https://github.com/maximilionus/Telemonitor/releases/tag/v0.0.1) (2020-06-26)

### Added
- Bot functionality done
- Added whitelist
- Added configuration file r/w


# Development Releases


## **4.0.0**-devN


### Added
- New optional startup argument `-y` or `--yes` for giving automatic confirmation to any user action request.

### Changed
- Systemd service CLI was remade to more user-friendly variant
  - Startup argument renamed from `--systemd-service` to `service`
  - Help for `service` usage
  - Enhanced output for `service`: `install` and `status` commands
  - Fixed `service upgrade` behaviour
- Enhanced *systemd service* launch script
  - Support for native virtual environment start
  - More detailed output
  - Usage documentation
- Core was split from a single `core.py` module to sorted by functionality modules in directory `core`


## [**4.0.0-dev1**](https://github.com/maximilionus/Telemonitor/releases/tag/v4.0.0-dev1)

### Added
- Feature to start **Telemonitor** with native python `pip` *(No poetry)*
- Feature to change path to the `systemd` service launch `.sh` script with `--systemd-service apply` command to merge all changes to service file
- New command for starting the app with *poetry*: `poetry run telemonitor`. Old `poetry run telem` can still be used
- Logging system can now be fully disabled with `--no-logging` startup argument
- Path of the service launch script now will be showed in `--systemd-service status` output

### Fixed
- Fixed .service file formatting
- Fixed `--systemd-service upgrade` behavior

### Changed
- Code structure major changes:
  - Main launch script is now `__main__.py`
  - Bot-related part split to `bot.py`
  - Startup procedure split to `startup.py`
  - `helpers` module renamed to `core`
- Systemd `.service` file was upgraded to new version *(See [README](./README.md#systemd-service-control) for upgrade instructions)*
- Updated project dependencies to newer versions
