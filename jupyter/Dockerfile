
FROM jupyter/base-notebook:latest

RUN pip install --no-cache-dir \
    pandas \
    matplotlib \
    sqlalchemy \
    "psycopg[binary]"

WORKDIR /home/jovyan/work