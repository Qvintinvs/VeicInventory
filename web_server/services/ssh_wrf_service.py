from models.wrf_round import WRFRound
from paramiko import Transport

from .connection_settings import ConnectionSettings
from .sftp_namelist_sender import SFTPNamelistSender


class SSHWRFService:
    def __init__(self, settings: ConnectionSettings, namelist_remote_path: str):
        self.__settings = settings
        self.__remote_path = namelist_remote_path

    def process_in_the_server(self, a_scheduled_round: WRFRound):
        hostname, username, password = self.__settings

        if not hostname:
            raise Exception("Missing hostname")

        if not username:
            raise Exception("Missing username")

        with Transport(hostname) as protocol:
            protocol.connect(username=username, password=password)

            namelist_text = str(a_scheduled_round.namelist)

            sender = SFTPNamelistSender(protocol, namelist_text)

            sender.send_namelist_to(self.__remote_path)
