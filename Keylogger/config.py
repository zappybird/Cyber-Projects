import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")

KEYLOG_FILE = config.get("DEFAULT", "keylog_file", fallback="keyfile.txt")
