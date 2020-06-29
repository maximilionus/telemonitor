# Telemonitor Changelog

[**Unreleased**](https://github.com/maximilionus/Telemonitor)

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