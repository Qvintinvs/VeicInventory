from paramiko import SFTPClient, Transport

from .vasques_emission_namelist_creator import VasquesEmissionNamelistCreator


class SFTPNamelistSender:
    def __init__(
        self,
        stablished_protocol: Transport,
        namelist_content: VasquesEmissionNamelistCreator,
    ):
        self.__protocol = stablished_protocol
        self.__namelist = namelist_content

    def send_namelist_to(self, a_remote_path: str):
        sftp_channel = SFTPClient.from_transport(self.__protocol)

        if sftp_channel is None:
            raise Exception("Could not create the sftp channel")

        with sftp_channel, sftp_channel.open(a_remote_path, "w") as remote_file:
            namelist_text = self.__namelist.create_namelist()

            remote_file.write(namelist_text)
