INFORME TÉCNICO – PARCIAL 2 DE COMUNICACIONES
1. Introducción

En este parcial se realizó la implementación de una infraestructura de servicios utilizando contenedores Docker, con el objetivo de integrar diferentes herramientas de comunicación, administración, almacenamiento y análisis de información dentro de un mismo proyecto.

La idea principal fue construir una arquitectura en la cual varios servicios pudieran comunicarse entre sí utilizando redes internas de Docker, mientras que el acceso desde el equipo se realizara principalmente mediante un servidor Nginx encargado de recibir las peticiones HTTP y dirigirlas hacia el servicio correspondiente.

Los servicios utilizados fueron Nginx, Joomla, PostgreSQL, Jupyter y Grafana. Cada uno cumple una función específica dentro de la arquitectura. Nginx funciona como proxy inverso, Joomla como portal web, PostgreSQL como sistema de almacenamiento de datos, Jupyter como herramienta para realizar análisis mediante Python y Grafana como herramienta de visualización.

Uno de los requisitos importantes del parcial fue que el proyecto pudiera ser clonado en una máquina limpia y posteriormente ejecutado sin tener que realizar manualmente toda la configuración de los servicios. Por esta razón, se organizó el proyecto mediante un archivo docker-compose.yml, variables de entorno y diferentes archivos de configuración.

Durante la implementación también se presentaron algunos problemas relacionados principalmente con la creación de archivos en Windows, la estructura de carpetas y la configuración de los diferentes servicios. Estos problemas fueron solucionados durante el proceso de implementación y se documentan en este informe.

2. Objetivos
2.1. Objetivo general

Implementar una arquitectura de servicios contenerizados mediante Docker que permita integrar Nginx, Joomla, PostgreSQL, Jupyter y Grafana, estableciendo comunicación entre los diferentes servicios y permitiendo el análisis y visualización de registros de tráfico HTTP.

2.2. Objetivos específicos
Crear una estructura organizada de carpetas para almacenar las configuraciones de cada servicio.
Implementar los diferentes servicios utilizando Docker Compose.
Configurar Nginx como proxy inverso.
Implementar Joomla como portal web.
Utilizar PostgreSQL para almacenar los registros de las peticiones HTTP.
Utilizar Jupyter para realizar análisis de los datos almacenados.
Utilizar Grafana para generar visualizaciones de los registros.
Crear redes Docker para controlar la comunicación entre los contenedores.
Utilizar volúmenes para conservar la información de los servicios.
Documentar el proceso de implementación y los problemas encontrados.
Comprobar que la infraestructura pueda ser desplegada desde un repositorio en una máquina limpia.
3. Estructura general del proyecto

Para comenzar el desarrollo se creó un repositorio llamado:

parcial-redes-comunicaciones

Inicialmente el repositorio se había creado dentro de:

C:\Windows\System32

Sin embargo, esta ubicación no era adecuada debido a que corresponde a una carpeta del sistema operativo.

Por esta razón, se decidió mover el proyecto a la carpeta del usuario:

C:\Users\duvan\parcial-redes-comunicaciones

El movimiento permitió trabajar sobre una ubicación propia del usuario y evitar problemas de permisos relacionados con las carpetas del sistema.

Después de realizar el cambio se verificó el repositorio utilizando:

git status

De esta manera se comprobó que el repositorio Git continuaba funcionando después de mover la carpeta.

La estructura utilizada para el proyecto fue:

parcial-redes-comunicaciones
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
├── INFORME.md
│
├── nginx
│   └── default.conf
│
├── jupyter
│   ├── Dockerfile
│   └── notebooks
│       └── analisis_datos.ipynb
│
├── grafana
│   ├── dashboards
│   │   └── joomla_logs.json
│   │
│   └── provisioning
│       ├── dashboards
│       │   └── dashboard.yml
│       │
│       └── datasources
│           └── datasource.yml
│
└── scripts
    ├── 01-traffic.sql
    └── collect_logs.py

Esta organización permite separar la configuración de cada servicio y facilita que otra persona pueda entender la estructura del proyecto.

4. Configuración de las variables de entorno

Uno de los primeros archivos creados fue:

.env.example

Este archivo contiene las variables necesarias para configurar PostgreSQL, Joomla, Jupyter y Grafana.

Entre las variables utilizadas se encuentran:

POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
JOOMLA_DB_TYPE
JOOMLA_DB_HOST
JOOMLA_DB_PORT
JOOMLA_DB_NAME
JOOMLA_DB_USER
JOOMLA_DB_PASSWORD
JUPYTER_TOKEN
GRAFANA_ADMIN_USER
GRAFANA_ADMIN_PASSWORD

La ventaja de utilizar variables de entorno es que las credenciales y configuraciones no tienen que estar escritas directamente dentro de docker-compose.yml.

Posteriormente se creó el archivo local:

.env

mediante:

Copy-Item .env.example .env

El archivo .env se utiliza para ejecutar el proyecto localmente, mientras que .env.example sirve como plantilla para que otra persona pueda crear su propia configuración.

También se creó un .gitignore para evitar que .env sea enviado al repositorio.

5. Configuración de Nginx

Nginx se utilizó como punto de entrada de la infraestructura.

El archivo utilizado fue:

nginx/default.conf

La función principal de Nginx es recibir las peticiones HTTP y determinar hacia qué servicio deben ser enviadas.

La arquitectura utiliza las siguientes rutas:

http://localhost/

para Joomla,

http://localhost/jupyter/

para Jupyter,

y:

http://localhost/grafana/

para Grafana.

De esta forma, desde el navegador se utiliza un único punto de acceso.

Por ejemplo, una petición dirigida a:

/jupyter/

es enviada internamente hacia:

jupyter:8888

Mientras que las peticiones hacia:

/grafana/

son enviadas hacia:

grafana:3000

Esto permite evitar que cada servicio tenga que publicar directamente su puerto en el computador.

6. Configuración de Jupyter

Para Jupyter se creó un archivo:

jupyter/Dockerfile

El Dockerfile utiliza como base:

FROM jupyter/base-notebook:latest

y posteriormente instala las bibliotecas necesarias para el análisis:

pandas
matplotlib
sqlalchemy
psycopg

Estas bibliotecas permiten trabajar con los datos almacenados en PostgreSQL y generar gráficas.

Problema encontrado durante esta etapa

Durante la creación del Dockerfile apareció un problema debido a Windows.

Al intentar verificar el archivo mediante:

Get-Content .\jupyter\Dockerfile

PowerShell indicó que el archivo no existía.

Después de revisar la carpeta se encontró que el archivo realmente había sido creado como:

Dockerfile.txt

Esto ocurre porque el Bloc de notas puede agregar automáticamente la extensión .txt.

Solución

Se corrigió el nombre utilizando:

Rename-Item ".\jupyter\Dockerfile.txt" "Dockerfile"

Posteriormente se verificó:

Get-ChildItem .\jupyter

y finalmente:

Get-Content .\jupyter\Dockerfile

Con esto se comprobó que el archivo tenía el nombre correcto y que Docker podría utilizarlo durante la construcción de la imagen.

Este fue uno de los problemas prácticos más importantes encontrados durante la organización de los archivos, ya que aunque el contenido estaba correcto, Docker no podía encontrarlo debido a la extensión adicional.

7. Cuaderno de análisis de datos

Dentro de:

jupyter/notebooks

se creó:

analisis_datos.ipynb

El cuaderno está diseñado para conectarse a PostgreSQL mediante SQLAlchemy.

La conexión utiliza como host:

database

Esto es posible porque Docker proporciona resolución de nombres entre los contenedores conectados a la misma red.

El cuaderno consulta la tabla:

nginx_requests

y obtiene información como:

fecha y hora de la petición;
dirección IP;
método HTTP;
ruta solicitada;
código de respuesta;
cantidad de bytes enviados.

Posteriormente se utilizan los datos para generar estadísticas y gráficas.

Por ejemplo, se realiza un análisis de las peticiones agrupadas por código HTTP y también de las direcciones IP que realizan mayor cantidad de peticiones.

8. PostgreSQL y almacenamiento de registros

PostgreSQL se utilizó como base de datos del proyecto.

Para almacenar los registros de Nginx se creó el archivo:

scripts/01-traffic.sql

En este archivo se define la tabla:

nginx_requests

La tabla contiene los campos:

id
ts
client_ip
method
path
status
bytes_sent

Cada uno almacena información diferente de las peticiones HTTP.

Por ejemplo:

client_ip

almacena la dirección IP que realizó la petición.

Mientras que:

status

almacena el código HTTP generado por el servidor.

También se crearon índices para mejorar las consultas relacionadas con el tiempo y los códigos de respuesta.

9. Recolección de los registros de Nginx

Para pasar los registros desde Nginx hasta PostgreSQL se creó:

scripts/collect_logs.py

Este programa utiliza Python y la biblioteca psycopg.

El funcionamiento general es:

Nginx
   ↓
access.log
   ↓
collect_logs.py
   ↓
PostgreSQL
   ↓
nginx_requests

El programa permanece ejecutándose y espera nuevas líneas en:

/var/log/nginx/access.log

Cuando aparece una nueva petición, el programa analiza el registro mediante una expresión regular.

Después extrae:

IP
fecha
método
ruta
código HTTP
bytes

y los inserta en PostgreSQL.

Una ventaja de esta solución es que no fue necesario crear un sexto contenedor exclusivamente para realizar la recolección, ya que el script se ejecuta dentro del contenedor de Jupyter.

10. Configuración de Grafana

Grafana se utilizó para visualizar los datos almacenados en PostgreSQL.

Se configuró una fuente de datos mediante:

grafana/provisioning/datasources/datasource.yml

La conexión apunta a:

database:5432

Esto permite que Grafana se comunique directamente con PostgreSQL mediante la red interna de Docker.

También se creó:

grafana/provisioning/dashboards/dashboard.yml

Este archivo permite que Grafana cargue automáticamente el dashboard sin que sea necesario crearlo manualmente cada vez que se levanta el proyecto.

El dashboard utilizado fue:

grafana/dashboards/joomla_logs.json

Se configuraron dos visualizaciones principales:

Peticiones HTTP agrupadas por código de respuesta.
Direcciones IP con mayor cantidad de peticiones.

Esto permite observar el tráfico generado durante las pruebas del portal.

11. Docker Compose

El archivo principal del proyecto es:

docker-compose.yml

Este archivo permite levantar toda la infraestructura de forma conjunta.

Los servicios definidos son:

nginx
database
joomla
jupyter
grafana

La arquitectura general puede representarse así:

                    INTERNET / HOST
                         │
                         │ HTTP :80
                         ▼
                    ┌─────────┐
                    │  NGINX  │
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      ┌────────┐    ┌─────────┐    ┌─────────┐
      │ Joomla │    │ Jupyter │    │ Grafana │
      └────┬───┘    └────┬────┘    └────┬────┘
           │             │              │
           └─────────────┼──────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ PostgreSQL  │
                  └─────────────┘
12. Redes Docker

Se definieron dos redes:

frontend_net

y:

backend_net

La red frontend_net permite la comunicación entre Nginx y los servicios que deben ser accesibles mediante el proxy.

La red backend_net se utiliza para las comunicaciones internas con PostgreSQL.

Esta separación permite organizar mejor el tráfico entre los contenedores.

Además, backend_net se configuró como una red interna:

internal: true

De esta forma se busca evitar que los servicios conectados a esta red tengan acceso directo desde el exterior.

13. Volúmenes Docker

También se utilizaron volúmenes para conservar información.

Entre ellos:

postgres_data
joomla_data
grafana_data
nginx_logs

Estos volúmenes tienen diferentes funciones.

postgres_data permite conservar la información de PostgreSQL.

joomla_data conserva los archivos del portal.

grafana_data conserva la información de Grafana.

nginx_logs permite compartir los registros de Nginx con el contenedor de Jupyter para que puedan ser procesados.

Esto es importante porque los contenedores pueden detenerse y volver a iniciarse sin perder automáticamente toda la información almacenada.

14. Problemas encontrados y soluciones

Durante la realización del proyecto se presentaron varios problemas de configuración.

14.1. Repositorio creado en una carpeta incorrecta

Inicialmente el repositorio se encontraba en:

C:\Windows\System32

Esto no era conveniente porque se trata de una carpeta protegida del sistema.

Solución

Se movió el proyecto a:

C:\Users\duvan\parcial-redes-comunicaciones

y posteriormente se verificó que Git continuara funcionando.

14.2. Archivos creados con extensión .txt

Uno de los problemas encontrados fue la creación del Dockerfile como:

Dockerfile.txt

en lugar de:

Dockerfile

Esto provocaba que el comando:

Get-Content .\jupyter\Dockerfile

generara un error indicando que la ruta no existía.

Solución

Se utilizó:

Rename-Item ".\jupyter\Dockerfile.txt" "Dockerfile"

Después se verificó nuevamente la carpeta y el contenido.

Este problema permitió comprobar la importancia de revisar siempre la extensión real de los archivos cuando se trabaja desde Windows.

14.3. Organización de los archivos

Otro aspecto que requirió atención fue mantener cada archivo en la ubicación correcta.

Por ejemplo:

jupyter/Dockerfile

no puede quedar en:

jupyter/notebooks/

De la misma manera, los archivos de Grafana deben estar separados entre:

grafana/provisioning

y:

grafana/dashboards

La estructura de carpetas se fue comprobando utilizando comandos como:

Get-ChildItem

y:

Get-ChildItem .\jupyter

Esto permitió detectar errores de ubicación antes de intentar levantar Docker.

15. Validación del proyecto

Antes de ejecutar los contenedores se debe comprobar que Docker Desktop esté funcionando correctamente.

Se utilizarán los comandos:

docker --version

y:

docker compose version

Después se debe validar la estructura del archivo:

docker compose config

Este comando es importante porque permite detectar errores de sintaxis o variables antes de iniciar los contenedores.

Posteriormente se puede ejecutar:

docker compose up -d --build

El parámetro --build permite construir la imagen personalizada de Jupyter a partir del Dockerfile.

Finalmente se puede comprobar el estado mediante:

docker compose ps

y revisar los registros mediante:

docker compose logs --tail=100
16. Pruebas de funcionamiento

Una vez que los contenedores estén ejecutándose, se deben realizar diferentes pruebas.

Primero se accede al portal mediante:

http://localhost/

Al realizar varias peticiones se generan registros en Nginx.

Posteriormente se puede ingresar a:

http://localhost/jupyter/

para abrir el cuaderno:

analisis_datos.ipynb

Desde allí se pueden ejecutar las celdas que consultan PostgreSQL.

Finalmente se accede a:

http://localhost/grafana/

para comprobar el dashboard.

El objetivo es que las peticiones realizadas al portal aparezcan posteriormente en las visualizaciones de Grafana.

También se puede comprobar directamente la cantidad de registros almacenados utilizando:

docker compose exec database psql -U joomla_user -d joomla_db -c "SELECT COUNT(*) FROM nginx_requests;"

Al generar nuevas peticiones, el número de registros debe aumentar.

17. Análisis desde el modelo OSI

La implementación también permite relacionar la infraestructura con diferentes capas del modelo OSI.

17.1. Capa 7 – Aplicación

En esta capa se encuentran los protocolos y servicios utilizados directamente por las aplicaciones.

En el proyecto se utiliza principalmente HTTP para las comunicaciones entre el navegador y Nginx.

También intervienen las aplicaciones web Joomla, Jupyter y Grafana.

Los registros generados por Nginx contienen información de las peticiones HTTP, como:

método
ruta
código de respuesta
17.2. Capa 4 – Transporte

La comunicación utiliza principalmente TCP.

Entre los puertos utilizados por los servicios están:

80    → Nginx
5432  → PostgreSQL
8888  → Jupyter
3000  → Grafana

Sin embargo, no todos estos puertos se publican directamente al computador.

Los servicios internos pueden comunicarse mediante las redes Docker utilizando los nombres de los servicios.

17.3. Capa 3 – Red

Docker crea redes virtuales que permiten la comunicación entre los diferentes contenedores.

En este proyecto se utilizan:

frontend_net
backend_net

Además, Docker proporciona resolución de nombres interna, permitiendo utilizar nombres como:

database

en lugar de tener que conocer directamente la dirección IP del contenedor.

17.4. Capa 2 – Enlace de datos

Docker utiliza interfaces virtuales y bridges para conectar los diferentes contenedores.

Esto permite que los contenedores puedan comunicarse como si estuvieran conectados a una red virtual.

De esta manera, Docker crea una infraestructura de red independiente de la red física utilizada por el computador.

18. Cumplimiento del requisito de despliegue

Uno de los puntos más importantes del parcial es que el proyecto pueda ser utilizado desde una máquina limpia.

La idea es que una persona pueda clonar el repositorio y preparar las variables mediante:

git clone URL_DEL_REPOSITORIO
cd parcial-redes-comunicaciones
Copy-Item .env.example .env

y posteriormente ejecutar:

docker compose up -d

De esta manera, la configuración de los servicios se encuentra almacenada dentro del repositorio y Docker Compose se encarga de crear la infraestructura.

Este procedimiento evita tener que crear manualmente cada contenedor.

Además, los archivos de configuración de Nginx, Grafana, Jupyter y PostgreSQL se encuentran dentro del proyecto.

19. Conclusiones

Durante el desarrollo del parcial se logró estructurar una infraestructura basada en contenedores Docker para integrar diferentes servicios de comunicación y análisis de información.

La utilización de Docker Compose permitió organizar los servicios dentro de un único archivo de configuración, haciendo más sencillo el proceso de despliegue y reduciendo la necesidad de realizar configuraciones independientes en cada contenedor.

Uno de los aspectos que más problemas generó fue la creación y ubicación de los archivos en Windows. Un ejemplo fue el Dockerfile de Jupyter, que inicialmente quedó guardado como Dockerfile.txt. Este problema se solucionó cambiando el nombre del archivo y verificando nuevamente su contenido desde PowerShell.

También fue necesario corregir la ubicación inicial del repositorio, ya que había sido creado dentro de System32. Se trasladó a la carpeta del usuario para trabajar en una ubicación más apropiada y se comprobó posteriormente que Git continuara funcionando.

La arquitectura implementada permite que Nginx funcione como punto de entrada, mientras que Joomla, Jupyter y Grafana trabajan como servicios independientes. PostgreSQL se encarga de almacenar la información y los registros generados por Nginx son procesados mediante Python.

La integración de Jupyter y Grafana permite utilizar los mismos datos desde dos enfoques diferentes. Jupyter permite realizar un análisis más directo mediante Python, mientras que Grafana permite visualizar los resultados mediante dashboards.

Finalmente, el proyecto fue organizado pensando en el requisito de que otra persona pueda clonar el repositorio en una máquina limpia y levantar la infraestructura utilizando Docker Compose. Por esta razón, se incluyeron los archivos de configuración, las variables de entorno de ejemplo, el Dockerfile, los scripts, los dashboards y la documentación necesaria para realizar el despliegue.