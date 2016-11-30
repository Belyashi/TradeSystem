from threading import Thread
import time

from settings import HISTORY_UPDATE_TIMEDELTA
from .update import update_stocks_history

UPDATE_TIMEDELTA_SECONDS = HISTORY_UPDATE_TIMEDELTA.total_seconds()


class HistoryUpdater(object):
    def __init__(self):
        self._thread = Thread(target=self._loop)

    def run(self):
        self._thread.start()

    def _loop(self):
        while True:
            update_stocks_history()
            time.sleep(UPDATE_TIMEDELTA_SECONDS)
