
# Parcial 2 - Comunicaciones

Proyecto de despliegue multi-contenedor para Ingeniería Mecatrónica.

## Servicios

- Nginx: proxy inverso.
- Joomla: portal institucional.
- PostgreSQL: base de datos relacional.
- Jupyter: análisis de datos con Python.
- Grafana: dashboards y estadísticas de tráfico.

## Requisitos

- Git.
- Docker Desktop.
- Docker Compose.

## Despliegue

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd parcial-redes-comunicaciones
```

Preparar las variables:

```bash
cp .env.example .env
```

Iniciar:

```bash
docker compose up -d
```

## Direcciones

- Joomla: http://localhost/
- Jupyter: http://localhost/jupyter/
- Grafana: http://localhost/grafana/

## Verificación

```bash
docker compose ps
docker compose logs --tail=100
```

## Detener

```bash
docker compose down
```

Los volúmenes nombrados conservan los datos al detener
los servicios. No usar `docker compose down -v` si se
desea conservarlos.