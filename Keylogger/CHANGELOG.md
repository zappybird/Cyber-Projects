# Changelog

## [Unreleased]

### Improvements

- **Enhanced Error Handling**
  - Improved error handling in the `key_pressed` function to catch specific exceptions (e.g., `AttributeError`, `IOError`). This allows for more informative error messages and greater robustness in logging.

- **Logging to Console with Log Levels**
  - Integrated logging functionality using Python's built-in `logging` module. Added log levels (INFO, ERROR) to monitor application behavior and errors in real-time, improving debugging and transparency.

- **Configuration Management**
  - Introduced a configuration file (`config.ini`) using the `configparser` library to manage settings, making it easier to expand functionality in the future.

- **Unit Testing**
  - Added a new testing file (`test_logger.py`) containing unit tests for the logging functionality. This helps ensure that all parts of the application work as expected and facilitates future maintenance.

- **Documentation with Sphinx**
  - Set up Sphinx for generating documentation from docstrings, providing a professional appearance and enabling easy generation of HTML or PDF documentation.

## [Initial Release] - 2/6/2026
- Initial implementation of a simple keylogger using the `pynput` library.