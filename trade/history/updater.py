from threading import Thread
import time

from settings import HISTORY_UPDATE_TIMEDELTA
from .update import update_stocks_history

UPDATE_TIMEDELTA_SECONDS = HISTORY_UPDATE_TIMEDELTA.total_seconds()

SLEEP_PERIOD = 5.


class HistoryUpdater(object):
    def __init__(self):
        self._thread = Thread(target=self._loop)
        self._active = False

    def run(self):
        if not self._active:
            self._active = True
            self._thread.start()

    def stop(self):
        if self._active:
            self._active = False

    def _loop(self):
        while self._active:
            update_stocks_history()

            left_time = UPDATE_TIMEDELTA_SECONDS
            while self._active and left_time > 0:
                sleep_time = SLEEP_PERIOD if SLEEP_PERIOD <= left_time else left_time
                left_time -= sleep_time
                time.sleep(sleep_time)
