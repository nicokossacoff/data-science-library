***
# Instalar Airflow

Desde la terminal vamos a acceder a nuestro ambiente virtual y vamos a crear dos variables de ambiente:
```zsh
$ AIRFLOW_VERSION=2.10.5
$ PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
```

También vamos a crear una variable con la siguiente URL:
```zsh
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
```

Una vez definidas estas tres variables vamos a instalar Airflow usando `pip`:
```zsh
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

# ⚙️ Configuración

Por defecto, el directorio en donde se instala Airflow es `~/airflow`. Ahí vamos a encontrar el archivo `airflow.cfg`, que nos va a ser muy útil al momento de cambiar las configuraciones del sistema.

## 🔨 Preparar el entorno local

El primer paso es crear la base de datos. Por defecto, se crea una base de datos de `sqlite`.
```zsh
airflow db migrate
```

Luego, debemos crear un usuario para poder acceder a la aplicación web de Airflow:
```zsh
airflow users create 
	--username [-u] admin \
	--firstname [-f] Peter \
    --lastname [-l] Parker \
    --role [-r] Admin \
    --email [-e] spiderman@superhero.org
```

Al crear el usuario se nos va a pedir crear una contraseña, la cual vamos a necesitar para acceder a la aplicación.
El siguiente paso es levantar el servidor web con el siguiente comando:
```zsh
airflow webserver --port 8080
```

Abrimos otra ventana de la terminal (la actual va a estar bloqueada por el proceso que se está corriendo) y vamos a levantar el scheduler:
```zsh
airflow scheduler
```