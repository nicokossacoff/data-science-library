***
# Introducción

Como ya sabemos, las capas de una imagen son inmutables, es decir, no podemos crear, modificar o eliminar sus archivos al ejecutar un contenedor.
Es por eso que, durante la creación del contenedor, Docker se encarga de crear una capa de escritura llamada *Writable Container Layer*. Esta es la única capa que tiene permisos para modificar el file-system durante la ejecución del contenedor. Algunas de sus funciones son:
- Se encarga de guardar todas las modificaciones realizadas sobre el file-system del contenedor (i.e., si se agrega, modifica, o elimina algún archivo).
- Nos asegura que los archivos que modificamos al ejecutar el contenedor no están modificando la imagen base. Es decir, antes de modificar un archivo, Docker hace una copia en la capa de escritura y recién ahí lo modifica, manteniendo intactas las capas de la imagen.
	- Esto, a su vez, es lo que nos permite ejecutar varios contenedores simultáneamente a partir de una misma imagen.

Ahora, esta capa de escritura es única por cada contenedor. Esto quiere decir que esta capa, y todos las modificaciones que contiene, se pierde al eliminar el contenedor. Esto hace que sea muy difícil extraer los datos de un contenedor, o que varios contenedores compartan datos entre ellos.
Por suerte, Docker soporta distintos tipos de almacenamientos que nos permiten acceder a los datos del contenedor incluso después de haber eliminado el contenedor. Estos tipos de almacenamientos son:
- Un **volumen** es un sistema de almacenamiento gestionado por el Docker daemon que nos permite guardar los datos de un contenedor en nuestra maquina anfitriona, incluso luego de que el contenedor haya sido eliminado. Sin embargo, no se puede acceder o interactuar directamente con los datos. Para poder acceder a los datos, vamos a tener que montar el volumen en un nuevo contenedor.



