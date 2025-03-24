from multiprocessing import Process, Queue

from models.wrf_round import WRFRound

from .ssh_wrf_service import SSHWRFService


class WRFRoundsQueueWorker(Process):
    def __init__(self, rounds_queue: Queue, sending_service: SSHWRFService):
        super().__init__()
        self.__rounds_queue: Queue = rounds_queue
        self.__sending_service = sending_service

    def add_to_the_queue(self, a_wrf_round: WRFRound):
        self.__rounds_queue.put(a_wrf_round)

    def consume_a_round(self):
        try:
            earliest_round: WRFRound | None = self.__rounds_queue.get(timeout=10)
        except Exception:
            return

        if earliest_round:
            self.__sending_service.process_in_the_server(earliest_round)

    def run(self):
        while True:
            self.consume_a_round()
