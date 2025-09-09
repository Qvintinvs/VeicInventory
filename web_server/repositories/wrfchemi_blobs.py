from pathlib import Path

from minio import Minio


class MinioRepository:
    def __init__(self, client: Minio, bucket_name: str):
        self.__client = client
        self.__bucket_name = bucket_name

        # Cria o bucket se não existir
        if not self.__client.bucket_exists(bucket_name):
            self.__client.make_bucket(bucket_name)

    def upload_file(self, file_path: str, object_name: str | None = None) -> None:
        """Envia um arquivo local para o MinIO"""
        minio_path = Path(file_path)

        if object_name is None:
            object_name = minio_path.name

        self.__client.fput_object(self.__bucket_name, object_name, str(file_path))

    def download_file(self, object_name: str, dest_path: str) -> None:
        """Baixa um arquivo do MinIO"""
        self.__client.fget_object(self.__bucket_name, object_name, dest_path)

    def list_files(self, prefix: str = ""):
        """Lista arquivos no bucket"""
        return [
            obj.object_name
            for obj in self.__client.list_objects(self.__bucket_name, prefix=prefix)
        ]

    def delete_file(self, object_name: str) -> None:
        """Remove um arquivo do MinIO"""
        self.__client.remove_object(self.__bucket_name, object_name)
