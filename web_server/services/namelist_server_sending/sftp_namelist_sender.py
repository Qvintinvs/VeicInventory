from paramiko import SFTPClient, Transport


class SFTPNamelistSender:
    def __init__(
        self,
        stablished_protocol: Transport,
        namelist_content: str,
    ):
        self.__protocol = stablished_protocol
        self.__namelist = namelist_content

    def send_namelist_to(self, a_remote_path: str):
        sftp_channel = SFTPClient.from_transport(self.__protocol)

        if sftp_channel is None:
            raise Exception("Could not create the sftp channel")

        with sftp_channel, sftp_channel.open(a_remote_path, "w") as remote_file:
            remote_file.write(self.__namelist)
