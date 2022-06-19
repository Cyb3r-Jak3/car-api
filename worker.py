"""Simple worker to keep web dyno alive"""

import os
import time

import urllib.request

APP_NAME = os.getenv("HEROKU_APP_NAME", None)
SLEEP_TIME = int(os.getenv("SLEEP_TIME", "600"))


while True:
    time.sleep(SLEEP_TIME)
    urllib.request.urlopen(f"https://{APP_NAME}.herokuapp.com/")
