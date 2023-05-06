from flask import Flask
from threading import Thread
from .kream import login
import schedule
import time


app = Flask(__name__)


@app.route('/')
def home():
    return "I'm alive"


def run():
    app.run(host='0.0.0.0', port=80)


def kream_test():
    schedule.every(2).hours.do(login)
    while True:
        schedule.run_pending()
        time.sleep(1)


def keep_alive():
    flask_t = Thread(target=run)
    kream_t = Thread(target=kream_test)
    flask_t.start()
    kream_t.start()
