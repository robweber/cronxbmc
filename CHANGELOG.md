# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Version 0.1.6](https://github.com/robweber/cronxbmc/compare/matrix-0.1.5...robweber:matrix-0.1.6) - 2022-4-24

### Changed

- updated README with additional info
- revamped Travis CI build procedure so this can be pushed to the Kodi repo
- updated the settings to the new Kodi format

### Fixed

- the `msgstr` attribute of the default language file should be blank
- fixed module for importing within other addons - thanks @TermeHansen 

### Removed

- removed `__init__.py` files as these aren't needed with Python 3

## [Version 0.1.5](https://github.com/robweber/cronxbmc/compare/matrix-0.1.4...robweber:matrix-0.1.5) - 2022-2-1

### Added

- added support for JSON RPC commands. The entire JSON string must be put into the command window [examples](https://kodi.wiki/view/JSON-RPC_API/Examples)

### Changed

- `cron.xml` file now contains a `command_type` attribute for each job. This contains either built-in or json depending on the command type

## [Version 0.1.4](https://github.com/robweber/cronxbmc/compare/matrix-0.1.3...robweber:matrix-0.1.4) - 2021-2-19

### Added

- support for a ```run_if_skipped``` attribute. This is false for existing jobs but can be toggled. When set to true will run a job if the execution time was skipped when Kodi is not running.

## [Version 0.1.3](https://github.com/robweber/cronxbmc/compare/matrix-0.1.2...robweber:matrix-0.1.3) - 2021-1-4

### Changed

- updated croniter lib to 0.3.31, this fixes #18

### Fixes

- fixed issue with timezones and calcuting the next run time

## [Version 0.1.2](https://github.com/robweber/cronxbmc/compare/krypton-0.1.1...robweber:matrix-0.1.2)

### Changed

- updated badges in the README
- updated code for Python3 (Kodi Matrix v19)
- updated syntax for pep8

## [Version 0.1.1](https://github.com/robweber/cronxbmc/compare/krypton-0.1.0...robweber:krypton-0.1.1)

### Changed

- updated badges in the README

## [Version 0.1.0](https://github.com/robweber/cronxbmc/compare/jarvis-0.0.9...robweber:krypton-0.1.0)

### Added
- use dateutil import
- updated for krypton
- use strings.po file for language
- show regional timestamp
- moved changelog.txt to new format based on keepachangelog

### Changed

- calculate sleep time better
- log function is always DEBUG level by default (Kodi best practice). Previous was NOTICE.
- the job id now follows the job as soon as it's created until it's removed. No more changing based on it's position in the file.

### Removed

- removed old strings.xml language file

## Version 0.0.9

### Added
- added way to segment jobs between addons

## Version 0.0.8

### Changed
- hardcode path so it doesn't modify when scripting - thanks shnabz

## Version 0.0.7

### Added
- added sytanx check when adding cron job

## Version 0.0.6

### Removed
- remove python os file code and replace with xbmcvfs module

## Version 0.0.5

### Added
- added new GUI

### Changed
- minor bug fixes

### Removed
- removed old gui code

## Version 0.0.4

### Added
- updated to Helix only python version
- created CronManager class to handle CronJob functions
- add module extension point for inclusion in other addons

### Removed
- support for xbmc versions older than Helix

## Version 0.0.3

### Changed
should use xbmc.sleep

## Version 0.0.2

### Added
- merged in GUI windows created by Kr0nZ

## Version 0.0.1

### Added
- Addon created
