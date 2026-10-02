import os
import re
import time
from datetime import datetime

import psycopg

LOG_FILE = "/var/log/nginx/access.log"

pattern = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>.*?) HTTP/\S+" '
    r'(?P<status>\d{3}) (?P<bytes>\S+)'
)

conn = None

while conn is None:
    try:
        conn = psycopg.connect(
            host="database",
            port=5432,
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            connect_timeout=5
        )
    except Exception as exc:
        print("Esperando PostgreSQL:", exc, flush=True)
        time.sleep(5)

conn.autocommit = True
print("Recolector: conectado a PostgreSQL", flush=True)


def open_log():
    """Espera un archivo real (no un enlace simbólico) y lo abre."""
    while True:
        if os.path.exists(LOG_FILE) and not os.path.islink(LOG_FILE):
            handle = open(LOG_FILE, "r", encoding="utf-8", errors="replace")
            print("Recolector: leyendo", LOG_FILE, flush=True)
            return handle
        print("Esperando el archivo de logs real de Nginx...", flush=True)
        time.sleep(2)


log = open_log()
inode = os.fstat(log.fileno()).st_ino

while True:
    line = log.readline()

    if not line:
        time.sleep(1)
        try:
            if os.path.islink(LOG_FILE) or os.stat(LOG_FILE).st_ino != inode:
                log.close()
                log = open_log()
                inode = os.fstat(log.fileno()).st_ino
        except FileNotFoundError:
            log.close()
            log = open_log()
            inode = os.fstat(log.fileno()).st_ino
        continue

    match = pattern.match(line)

    if not match:
        continue

    data = match.groupdict()

    try:
        timestamp = datetime.strptime(
            data["time"], "%d/%b/%Y:%H:%M:%S %z"
        )

        bytes_sent = (
            0 if data["bytes"] == "-"
            else int(data["bytes"])
        )

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO nginx_requests
                (ts, client_ip, method, path, status, bytes_sent)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    timestamp,
                    data["ip"],
                    data["method"],
                    data["path"],
                    int(data["status"]),
                    bytes_sent
                )
            )

    except Exception as exc:
        print("Error procesando registro:", exc, flush=True)