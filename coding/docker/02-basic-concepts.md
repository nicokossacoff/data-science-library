***
# 📦 Contenedores

Los **contenedores** de Docker son ambientes aislados en donde podemos ejecutar nuestras aplicaciones y sus distintos componentes. Por ejemplo, podemos tener un contenedor para ejecutar el front-end que desarrollamos con React, otro contenedor para ejecutar el back-end que desarrollamos con Python, y otro contenedor para ejecutar nuestra base de datos de PostgreSQL. En ese caso, cada componente se va a ejecutar de manera aislada e independiente del resto.

## ✅ Ventajas

- La principal ventaja de los contenedores es que poseen todo lo necesario para ejecutar nuestra aplicación, sin ningún tipo de dependencia con la máquina anfitriona. Esto nos asegura que cada componente de nuestra aplicación se está ejecutando de manera aislada, sin ser afectada (o sin afectar) al resto de los componentes que se están ejecutando en otros contenedores.
- Se manejan de manera independiente. Esto quiere decir que si borramos un contenedor, los demás no se ven afectados.
- Son portables y se pueden ejecutar en cualquier computadora (ya sea local, en un servidor físico o en la nube).

## Ejecutar un contenedor

El comando para ejecutar un contenedor es el siguiente:
```zsh
docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```

Hay varios componentes importantes:
- Como veremos más adelante, para ejecutar un contenedor necesitamos una _imagen_ de referencia (el contenedor lo vamos a crear a partir de esta _imagen_).
	- El flag `IMAGE[:TAG|@DIGEST]` nos permite definir el nombre y el tag (versión) de la imagen a partir de la cual vamos crear el contenedor. Si no especificamos la versión, se utiliza la última versión disponible (`latest`).
	- Por ejemplo, si quisiéramos ejecutar un contenedor utilizando la versión `24.04` de Ubuntu, deberíamos ejecutar el siguiente comando: `docker run ubuntu:24.04`.
- `[OPTIONS]` nos permite configurar nuestro contenedor. Por ejemplo, podemos ejecutar nuestro contenedor como un proceso en background (`-d`, `--detach`) o  podemos ponerle un nombre (`--name`). La lista completa se encuentra en la [documentación](https://docs.docker.com/reference/cli/docker/container/run/).

## 📚 Recursos
- [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/). Docker docs.
- [Running containers](https://docs.docker.com/engine/containers/run/). Docker docs.
***

# Imágenes

