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
- Docker Desktop (abierto y con el motor funcionando).
- Docker Compose.
- Puerto 80 libre.

## Despliegue

Clonar el repositorio:

```bash
git clone https://github.com/camilopenagos1/parcial-redes-comunicaciones.git
cd parcial-redes-comunicaciones
```

Preparar las variables:

```bash
cp .env.example .env
```

En PowerShell:

```powershell
Copy-Item .env.example .env
```

Iniciar:

```bash
docker compose up -d
```

La primera vez tarda unos minutos porque descarga imágenes,
construye Jupyter e instala Joomla automáticamente.

## Direcciones y credenciales

- Joomla: http://localhost/
- Joomla administrador: http://localhost/administrator
  (usuario `duvan` / contraseña `Parcial_Comunicaciones02`)
- Jupyter: http://localhost/jupyter/
  (token `parcial2026`)
- Grafana: http://localhost/grafana/
  (usuario `duvan` / contraseña `Parcial_Comunicaciones02`)

## Verificación

```bash
docker compose ps
docker compose logs --tail=100
```

Para generar tráfico y ver datos en Grafana y Jupyter, abrir
http://localhost/ varias veces o ejecutar en PowerShell:

```powershell
1..30 | ForEach-Object { curl.exe -s -o NUL http://localhost/ }
```

## Detener

```bash
docker compose down
```

Los volúmenes nombrados conservan los datos al detener
los servicios. No usar `docker compose down -v` si se
desea conservarlos.