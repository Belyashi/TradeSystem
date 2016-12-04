from threading import Thread
import time
import logging

from settings import HISTORY_UPDATE_TIMEDELTA
from trade.stock_history.update import update_histories

UPDATE_TIMEDELTA_SECONDS = HISTORY_UPDATE_TIMEDELTA.total_seconds()

SLEEP_PERIOD = 5.


logger = logging.getLogger(__name__)


class StockHistoryUpdater(object):
    def __init__(self, session):
        self._session = session

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
            try:
                update_histories(self._session)
            except Exception as e:
                logger.exception(e)

            left_time = UPDATE_TIMEDELTA_SECONDS
            while self._active and left_time > 0:
                sleep_time = SLEEP_PERIOD if SLEEP_PERIOD <= left_time else left_time
                left_time -= sleep_time
                time.sleep(sleep_time)
