import pathlib
import subprocess
import time
import typing


def get_user():
    cmd = "who | awk '{print $1}' | sort | head -1"
    while True:
        name = subprocess.check_output(cmd, shell=True).decode().strip()
        if name not in [None, ""]:
            return name
        time.sleep(0.1)


CURRENT_USER = get_user()
BUDDY_API_VERSION = 5
CONFIG_VERSION_LITERAL = typing.Literal[26]
CONFIG_DIR = str(pathlib.Path("/home", CURRENT_USER, ".config", "moondeck"))
CONFIG_FILENAME = "settings.json"
LOG_FILE = "/tmp/moondeck.log"
RUNNER_LOG_FILE = "/tmp/moondeck-runner.log"
MOONLIGHT_LOG_FILE = "/tmp/moondeck-runner-moonlight.log"
RUNNER_RESULT_FILE = "/tmp/moondeck-runner.result"
