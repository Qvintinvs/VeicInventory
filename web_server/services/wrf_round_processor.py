from multiprocessing import Process, Queue

from models.wrf_round import WRFRound


class WRFRoundProcessor(Process):
    def __init__(self, rounds_queue: Queue):
        super().__init__()
        self.__queue = rounds_queue

    def enqueue_round(self, wrf_round: WRFRound):
        self.__queue.put(wrf_round)

    def send_next_round(self):
        try:
            earliest_round: WRFRound | None = self.__queue.get(timeout=10)
        except Exception:
            return

        if earliest_round:
            pass

    def run(self):
        while True:
            self.send_next_round()
