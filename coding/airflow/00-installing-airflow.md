***
# Instalación local

Primero es necesario crear un ambiente virtual para evitar problemas de dependencias. Una vez que creamos el ambiente virtual, lo primero que tenemos que hacer es definir tres variables:
```zsh
$ AIRFLOW_VERSION=2.10.5
$ PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
$ CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
```

El siguiente paso es instalar Airflow usando `pip`:
```zsh
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

## ⚙️ Configuración

Por defecto, Airflow se instala en el siguiente directorio: `~/airflow`. Ahí vamos a encontrar el archivo `airflow.cfg`, que nos va a ser muy útil al momento de modificar las configuraciones del sistema.

### 🔨 Preparar el entorno local

El primer paso es crear la base de datos. Por defecto, se crea una base de datos de `sqlite`[^1].
```zsh
airflow db migrate
```

El siguiente paso es crear el usuario para acceder a la UI web de Airflow. Se nos va a pedir crear una contraseña, la cual vamos a necesitar para logearnos.
```zsh
airflow users create 
	--username [-u] admin \
	--firstname [-f] Peter \
    --lastname [-l] Parker \
    --role [-r] Admin \
    --email [-e] spiderman@superhero.org
```

Activamos la UI web con el siguiente comando:
```zsh
airflow webserver --port 8080
```

Abrimos otra ventana de la terminal (la actual va a estar bloqueada por el proceso que se está corriendo) y vamos a activar el scheduler:
```zsh
airflow scheduler
```

[^1]: Podemos utilizar esta base de datos durante el desarrollo de nuestro pipeline. Sin embargo, para un ambiente productivos es necesario utilizar otro motor de base de datos, como PostgreSQL o MySQL.

***
# Instalación en VM

Supongamos que queremos ejecutar nuestro pipeline en una instancia de Compute Engine que utiliza Ubuntu 24.04. Para eso tenemos que instalar Airflow y todas sus dependencias.
Antes de comenzar con la instalación, es necesario actualizar el sistema e instalar las dependencias de Python básicas como `pip` y `virtualenv`:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv libpq-dev build-essential
```

Una vez hecho esto estamos preparados para instalar y configurar Airflow. Los pasos que tenemos que seguir son los siguientes:
1. Creamos un usuario dedicado para Airflow (si bien esto no es necesario, si es lo recomendado):
```bash
sudo useradd -m -s /bin/bash airflow
sudo passwd airflow
```
2. Creamos un ambiente virtual:
```bash
python3 -m venv
source ~/venv/bin/activate
```
3. Creamos un directorio para instalar Airflow. Notar que definimos una variable de entorno, `AIRFLOW_HOME`, que especifica el directorio en donde queremos instalar Airflow. 
```bash
mkdir ~/airflow
AIRFLOW_HOME=~/airflow
echo 'export AIRFLOW_HOME=~/airflow' >> ~/.bashrc
```
4. Instalamos Airflow de la misma forma que cuando lo instalamos local. Primero definimos algunas variables de entorno y luego instalamos Airflow usando `pip`.
```bash
AIRFLOW_VERSION=2.10.5
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
```

```bash
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```
5. Como base de datos vamos a utilizar una instancia de Cloud SQL (es donde Airflow va a guardar la metadata). Es necesario primero tener creada y configurada la instancia de Cloud SQL.
   Para configurar la base de datos, tenemos que acceder al archivo de configuración (`~/airflow/airflow.cfg`) y buscar el parámetro `sql_alchemy_conn`, el cual define la conexión entre Airflow y la base de datos.
	- Hay varias formas para conectarnos a nuestra base de datos, pero la más recomendada es utilizar Cloud SQL Auth Proxy, ya que nos asegura una conexión segura. En esta sección se explica como se configura.
	- Si nuestra base de datos es PostgreSQL (recomendado), definimos:
```
sql_alchemy_conn = postgresql+psycopg2://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME
```
6. Una vez configurada la base de datos en Airflow, instalamos las dependencias necesarias para poder conectarnos desde la máquina virtual:
```bash
source ~/venv/bin/activate
pip install psycopg2-binary apache-airflow[postgres]
```
7. Finalmente, inicializamos nuestra base de datos:
```bash
airflow db init
```
8. Creamos el usuario administrador:
```
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password your_secure_password
```
9. Iniciamos Airflow ejecutando (en terminales separadas) los comandos `airflow webserver` y `airflow scheduler`. Otra opción, recomendada para ambientes productivos, es crear un servicio para que `systemd` manejo estos procesos por nosotros.

## Configurar Cloud SQL Proxy
- Lo primero que tenemos que hacer es instalar Cloud SQL Auth Proxy en nuestra máquina virtual:
```bash
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.4.0/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy
```
- Luego, desde la consola de Google Cloud obtenemos el nombre de la conexión a Cloud SQL (usualmente es `project-id:region:instance-name`).
- Ejecutamos el proxy:
```bash
./cloud-sql-proxy --port=5432 INSTANCE_CONNECTION_NAME &
```

## Configurar los servicios `systemd`

Para que `systemd` ejecute Airflow por nosotros tenemos que primero crear dos servicios, uno para el servidor web y otro para el scheduler.

### Crear un servicio para el servidor web de Airflow

- Creamos el archivo `airflow-webserver.service` ejecutando el siguiente comando:
```bash
sudo nano /etc/systemd/system/airflow-webserver.service
```
- Agregamos el siguiente contenido, reemplazando `YOUR_USERNAME` por el nombre de usuario y `YOUR_GROUP` por el nombre del grupo de usuarios (para validar el grupo se puede ejecutar el siguiente comando ``id -gn``): 
```bash
[Unit]
Description=Airflow webserver
After=network.target

[Service]
User=YOUR_USERNAME
Group=YOUR_GROUP
Type=simple
ExecStart=/home/YOUR_USERNAME/venv/bin/airflow webserver
Restart=on-failure
RestartSec=5s
PrivateTmp=true 

[Install]
WantedBy=multi-user.target
```

### Crear un servicio para el scheduler

- Creamos el archivo `airflow-scheduler.service` ejecutando el siguiente comando:
```bash
sudo nano /etc/systemd/system/airflow-scheduler.service
```
- Agregamos el siguiente contenido. Al igual que antes, debemos reemplazar `YOUR_USERNAME` y `YOUR_GROUP` por los valores correspondientes.
```bash
[Unit]
Description=Airflow scheduler
After=network.target

[Service]
User=YOUR_USERNAME
Group=YOUR_GROUP
Type=simple
ExecStart=/home/YOUR_USERNAME/venv/bin/airflow scheduler
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Iniciar los servicios

Una vez que hayamos creado los servicios, tenemos que correr los siguientes comandos:
1. Este comando reinicia `systemd`. Si no lo reiniciamos, entonces no podrá reconocer los nuevos servicios que creados.
```bash
sudo systemctl daemon-reload
```
2. Este comando habilita que tanto el servidor web como el scheduler de Airflow se puedan ejecutar al inicializar el sistema. Sin embargo, esto NO inicia los servicios, solo nos asegura que se van a ejecutar cuando volvamos a inicializar el sistema.
```bash
sudo systemctl enable airflow-webserver airflow-scheduler
```
3. Este comando es el que inicializa ambos servicios.
```bash
sudo systemctl start airflow-webserver airflow-scheduler
```