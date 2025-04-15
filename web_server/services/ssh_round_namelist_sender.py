from models.wrf_round import WRFRound
from paramiko import Transport

from .sftp_namelist_sender import SFTPNamelistSender
from .wrf_remote_connection_settings import WRFRemoteConnectionSettings


class SSHRoundNamelistSender:
    def __init__(
        self,
        connection_settings: WRFRemoteConnectionSettings,
        namelist_remote_path: str,
    ):
        self.__settings = connection_settings
        self.__remote_path = namelist_remote_path

    def upload_namelist_for_round(self, scheduled_round: WRFRound):
        hostname, username, password = self.__settings

        if not hostname:
            raise Exception("Missing hostname")

        if not username:
            raise Exception("Missing username")

        with Transport(hostname) as protocol:
            protocol.connect(username=username, password=password)

            namelist_text = str(scheduled_round.namelist)

            sender = SFTPNamelistSender(protocol, namelist_text)

            sender.upload_namelist_via_sftp(self.__remote_path)
