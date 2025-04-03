from multiprocessing import Process, Queue

from models.wrf_round import WRFRound

from .ssh_wrf_service import SSHRoundNamelistSender


class WRFRoundProcessor(Process):
    def __init__(self, rounds_queue: Queue, sending_service: SSHRoundNamelistSender):
        super().__init__()
        self.__queue = rounds_queue
        self.__sender = sending_service

    def enqueue_round(self, wrf_round: WRFRound):
        self.__queue.put(wrf_round)

    def send_next_round(self):
        try:
            earliest_round: WRFRound | None = self.__queue.get(timeout=10)
        except Exception:
            return

        if earliest_round:
            self.__sender.send_to_remote_server(earliest_round)

    def run(self):
        while True:
            self.send_next_round()
