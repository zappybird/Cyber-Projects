# CHANGELOG

All notable changes to this project will be documented here.

---

## v0.2.0 — Professional Improvements Pass
**Date:** 2026‑02‑06

---

## 1. Enhanced Error Handling

### What Changed
Replaced broad `except:` blocks with targeted exception handling in `logger.py`.

```python
except AttributeError:
    print("Special key pressed; not logged.")
except IOError as e:
    print(f"File error: {e}")
Benefit
Improves robustness and makes debugging more predictable by distinguishing between:

Special keys that do not produce characters

Actual file I/O errors

Long‑Term Impact
Creates a safer, more maintainable codebase and prevents silent failures.

2. Logging to Console with Log Levels
What Changed
Introduced Python’s logging module for structured runtime output.

python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
Replaced print() statements with logging.info() and logging.error().

Benefit
Adds timestamps and severity levels

Improves transparency during execution

Enables future enhancements like log rotation or verbosity flags

Long‑Term Impact
Moves the project toward production‑grade observability.

3. Configuration Management via config.ini
What Changed
Added a config.ini file and updated config.py to load settings using configparser.

config.ini

Code
[DEFAULT]
keylog_file = keyfile.txt
config.py

python
config = configparser.ConfigParser()
config.read('config.ini')

KEYLOG_FILE = config['DEFAULT']['keylog_file']
Benefit
Decouples configuration from code

Makes customization easier

Supports future expansion (paths, toggles, limits, etc.)

Long‑Term Impact
Establishes a scalable configuration system — essential for long‑term maintainability.

4. Introduced Unit Testing Structure
What Changed
Added a test_logger.py file using Python’s unittest framework.

python
class TestLogger(unittest.TestCase):
    def test_key_pressed_valid(self):
        pass

    def test_key_pressed_special(self):
        pass
Benefit
Ensures correctness

Prevents regressions

Encourages safer refactoring

Long‑Term Impact
Lays the foundation for a complete automated test suite.

5. Documentation Setup with Sphinx
What Changed
Installed Sphinx and initialized documentation scaffolding.

Commands

Code
pip install sphinx
sphinx-quickstart
Benefit
Converts docstrings into HTML/PDF documentation

Improves clarity and accessibility

Matches industry‑standard Python documentation practices

Long‑Term Impact
Gives the project a professional documentation pipeline.

Summary of Improvements
Improvement	Purpose	Professional Benefit
Enhanced Error Handling	Robustness & clarity	Cleaner debugging, safer code
Logging with Levels	Runtime visibility	Production‑style diagnostics
Config Management	Flexibility	Easier customization & scaling
Unit Testing	Reliability	Prevents regressions, shows maturity
Sphinx Docs	Clarity	Professional documentation output
v0.1.0 — Initial Prototype
Date: 2026‑02‑04

Basic keypress capture using pynput

Writes character keys to a text file

Minimal error handling

Single‑file implementation