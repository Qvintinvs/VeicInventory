from io import BytesIO

import zstandard as zstd
from minio import Minio


class MinioRepository:
    def __init__(self, client: Minio, bucket_name: str):
        self.__client = client
        self.__bucket_name = bucket_name

        # Cria o bucket se não existir
        if not self.__client.bucket_exists(bucket_name):
            self.__client.make_bucket(bucket_name)

    def download_file(self, object_name: str, dest_path: str) -> None:
        """Baixa um arquivo do MinIO"""
        self.__client.fget_object(self.__bucket_name, object_name, dest_path)

    def list_files(self, prefix: str = ""):
        """Lista arquivos no bucket"""
        return (
            obj.object_name
            for obj in self.__client.list_objects(self.__bucket_name, prefix=prefix)
        )

    def read_file(self, prefix: str):
        response = self.__client.get_object(
            self.__bucket_name, f"wrfchemi/{prefix}.zst"
        )

        compressed_data = response.read()

        response.close()
        response.release_conn()

        dctx = zstd.ZstdDecompressor()
        decompressed_data = dctx.decompress(compressed_data)

        return BytesIO(decompressed_data)

    def delete_file(self, object_name: str) -> None:
        """Remove um arquivo do MinIO"""
        self.__client.remove_object(self.__bucket_name, object_name)
