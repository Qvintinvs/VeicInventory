from multiprocessing import Process, Queue

from models.wrf_round import WRFRound

from .ssh_wrf_service import SSHWRFService


class RoundsQueueWorker(Process):
    __round_queue: Queue[WRFRound | None] = Queue()

    def __init__(self, sending_service: SSHWRFService):
        self.__sending_service = sending_service

        super().__init__()

    def add_to_the_queue(self, a_wrf_round: WRFRound):
        self.__round_queue.put(a_wrf_round)

    def consume_latest_round(self):
        try:
            latest_round = self.__round_queue.get(timeout=10)
        except Exception:
            return

        if latest_round:
            self.__sending_service.process_in_the_server(latest_round)

    def run(self):
        while True:
            self.consume_latest_round()
