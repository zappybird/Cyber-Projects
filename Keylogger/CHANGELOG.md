# Changelog

## [Unreleased]

### Added — 2026-02-06 21:10 EST
- **Word Grouping Logic**
  - Implemented intelligent word buffering that groups characters into words.
  - Words now end when the user presses space or pauses typing for more than 1 second.

- **Single Timestamp per Word**
  - Each completed word is logged with one timestamp instead of timestamping every character.

- **Flush-on-Exit Behavior**
  - Added `flush_on_exit()` to ensure the final word is written when ESC is pressed.

### Improvements — 2026-02-06 21:10 EST
- **Robust Space Detection**
  - Space detection now handles `Key.space`, literal `" "`, and cases where `char` is `None`.

- **Improved Special Key Handling**
  - Special keys no longer cause crashes or undefined behavior.
  - Fixed `UnboundLocalError` caused by referencing `char` before assignment.

- **Stability Fixes**
  - Ensured the listener remains active by returning `True` for all non‑ESC keys.
  - Improved shutdown behavior and prevented premature termination.

- **Refactored Logging Flow**
  - Simplified and clarified the logic inside `key_pressed`.
  - Improved readability and maintainability of the core logging engine.

- **Updated README**
  - Added Project Structure and How It Works sections.
  - Improved clarity, formatting, and educational framing.

### Previous Improvements — 2026-02-06 17:00 EST
- **Enhanced Error Handling**
  - Improved error handling in the `key_pressed` function to catch specific exceptions (e.g., `AttributeError`, `IOError`).

- **Logging to Console with Log Levels**
  - Integrated logging functionality using Python's built-in `logging` module.

- **Configuration Management**
  - Introduced a configuration file (`config.ini`) using the `configparser` library.

- **Unit Testing**
  - Added a new testing file (`test_logger.py`) containing unit tests for logging functionality.


## [Initial Release] — 2026-02-06 13:00 EST
- Initial implementation of a simple keylogger using the `pynput` library.
