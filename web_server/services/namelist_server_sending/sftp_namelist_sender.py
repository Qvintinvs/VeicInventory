from io import BytesIO

from paramiko import SFTPClient, Transport


class SFTPNamelistSender:
    def __init__(self, stablished_protocol: Transport, namelist_file_bytes: BytesIO):
        self.__protocol = stablished_protocol
        self.__file_bytes = namelist_file_bytes

    def send_namelist_to(self, a_remote_path: str):
        sftp_channel = SFTPClient.from_transport(self.__protocol)

        if sftp_channel is None:
            raise Exception("Could not create the sftp channel")

        with sftp_channel:
            sftp_channel.putfo(self.__file_bytes, a_remote_path)
