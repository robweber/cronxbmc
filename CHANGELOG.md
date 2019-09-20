# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased](https://github.com/robweber/cronxbmc/compare/73362e5...HEAD)

### Added
- use dateutil import
- updated for krypton
- show regional timestamp
- moved changelog.txt to new format based on keepachangelog

### Changed

- calculate sleep time better

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
