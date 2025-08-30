import json
import os
import time
from typing import Union, cast

import redis

r = redis.Redis(host="localhost", port=6379)

queue_name = "wrf-queue"

run_script_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "fortran", "run.sh")
)

env = os.environ.copy()

print("Aguardando round na fila...")


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
    output = os.read(r_fd, 65535).decode()
    os.close(r_fd)

    # Espera o processo terminar
    _, status = os.waitpid(pid, 0)

    return status, output


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
    else:
        time.sleep(1)
