import io
import json
import os
import time
from typing import Union, cast

import boto3
import redis
import zstandard as zstd
from dotenv import load_dotenv

from db import session
from file import File

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

r = redis.from_url(REDIS_URL)

queue_name = "wrf-queue"

run_script_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "fortran", "run.sh")
)

env = os.environ.copy()

print("Aguardando round na fila...")

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)  # nosec


def upload_to_minio(file_bytes, bucket_name: str, object_key: str):
    fileobj = io.BytesIO(file_bytes)  # transforma bytes em "arquivo em memória"
    s3.upload_fileobj(fileobj, bucket_name, object_key)


def compress_file(path: str):
    with open(path, "rb") as f:
        data = f.read()

    cctx = zstd.ZstdCompressor(level=3)  # ajuste nível conforme tradeoff

    return cctx.compress(data)


def insert_round_wrfem_output():
    load_dotenv()  # carrega variáveis do .env

    file_00to12_path = os.getenv("WRFEM_OUTPUT_00TO12")
    file_12to24_path = os.getenv("WRFEM_OUTPUT_12TO24")

    if not file_00to12_path or not file_12to24_path:
        raise ValueError("Caminhos dos arquivos não configurados no .env")

    new_file1: File = File(
        name="wrfem_00to12z_d01", data=compress_file(file_00to12_path)
    )
    new_file2: File = File(
        name="wrfem_12to24z_d01", data=compress_file(file_12to24_path)
    )

    session.add(new_file1)
    session.add(new_file2)
    session.commit()

    object_key1 = f"wrfchemi/round_{new_file1.id}.zst"
    object_key2 = f"wrfchemi/round_{new_file1.id}.zst"

    upload_to_minio(new_file1.data, "wrfchemi-blobs", object_key1)
    upload_to_minio(new_file2.data, "wrfchemi-blobs", object_key2)


def run_and_capture():
    r_fd, w_fd = os.pipe()

    actions = (
        (os.POSIX_SPAWN_DUP2, w_fd, 1),  # dup2(w_fd, STDOUT_FILENO)
        (os.POSIX_SPAWN_DUP2, w_fd, 2),  # dup2(w_fd, STDERR_FILENO)
        (os.POSIX_SPAWN_CLOSE, r_fd),  # Fecha r_fd no filho
        (os.POSIX_SPAWN_CLOSE, w_fd),  # Fecha w_fd no filho
    )

    pid = os.posix_spawn(run_script_path, ("/bin/bash",), env, file_actions=actions)

    # Fecha o lado de escrita no pai
    os.close(w_fd)

    # Lê toda a saída
    output = b"".join(iter(lambda: os.read(r_fd, 4096), b""))

    # Fecha o lado de leitura no pai
    os.close(r_fd)

    _, status = os.waitpid(pid, 0)

    return status, output.decode()


while True:
    item = cast(Union[bytes, None], r.lpop(queue_name))

    if item:
        try:
            text = item.decode("utf-8")

            json_object = json.loads(text)

            print("Round recebido:")
            print(json.dumps(json_object, indent=4))
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", e)

            continue

        print("Executando run.sh...")

        if not os.access(run_script_path, os.X_OK):
            print(f"Erro: run.sh não é executável.\n{run_script_path}")

            exit(1)

        # Executa o script e mostra a saída
        status, output = run_and_capture()

        print(f"Saída do run.sh:\n{output}")

        if status:
            print(f"Erros do run.sh:\n{status}")

        insert_round_wrfem_output()
    else:
        time.sleep(1)
