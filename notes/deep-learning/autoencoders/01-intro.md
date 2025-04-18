***
# Introducción

Los **autoencoders** son redes neuronales cuya tarea de pretexto es reconstruir los inputs que recibe. Su estructura consiste de dos partes:
- La primer parte se conoce como **encoder**, y se encarga de aprender una representación de los inputs, $h=f(x)$.
- La segunda parte se conoce como **decoder**, y se encarga de reconstruir los inputs a partir de la representación que aprende el encoder, $r=g(h)$.

Gráficamente, la estructura de un autoencoder se puede representar de la siguiente manera:
![autoencoders-computer-vision](attachments/autoencoders-computer-vision.png)
Al ser redes neuronales **feed-forward**, se entrenan usando las mismas técnicas que usamos para un MLP tradicional. Entonces, vamos a utilizar **back-propagation** para calcular los gradientes y **stochastic gradient descent** (o cualquier otro algoritmo de optimización) para ajustar los pesos.

Ahora, un modelo cuya función es reconstruir los inputs que recibe no es particularmente útil. Lo que ocurre es que la tarea de reconstrucción es solo una tarea de pretexto, y lo que esperamos al entrenar un autoencoder es que la representación $h$ que aprende el modelo contenga información valiosa sobre nuestros datos.
Cómo nos podemos asegurar de que el modelo aprenda esta información? Por lo general, diseñamos los autoencoders para que no puedan reconstruir los inputs a la perfección mediante algún tipo de restricción. Al restringir el modelo, lo que logramos es que se concentre en las características más importantes para la reconstrucción.
## Estructura: profundidad y tamaño de las capas ocultas

El **Teorema de Aproximación Universal** nos garantiza que una red neuronal con al menos una capa oculta puede representar, con un nivel de precisión arbitrario, cualquier función no lineal, siempre y cuando tenga la suficiente cantidad de neuronas.
Entonces, en principio, un encoder con una única capa oculta es suficiente para aprender la representación $h$. Sin embargo, no solo estará limitado en el tipo de transformaciones que puede aprender, sino que tampoco será capaz de forzar ciertas propiedades sobre esa representación $h$. Agregar más capas ocultas a nuestro encoder nos permitiría aprender transformaciones más complejas y forzar propiedades sobre la representación $h$ (e.g., para forzar que sea esparsa).

Por último, una mayor profundidad nos permite reducir los costos computacionales de aproximar algunas funciones (i.e., cuantas más capas ocultas tengamos, menos neuronas necesitamos por capa, lo que reduce la cantidad de pesos en nuestra red neuronal) y nos permite reducir la cantidad de datos de entrenamientos necesarios.
## Encoders y Decoders Estocásticos

Una estrategia muy común al diseñar las unidades de salida y la función de pérdida de una red neuronal es definir una distribución para el output, $P(y|x)$. La función de perdida es igual a menos la log-verosimilitud de la distribución, $-\log{P(y|x)}$. Por ejemplo, para los casos de clasificación binaria, la función de pérdida (i.e., menos la log-verosimilitud) es la entropía cruzada binaria, la cual se obtiene de asumir que $P(y|x)$ sigue una distribución Bernoulli.
Podemos aplicar esta misma técnica para entrenar los autoencoders. Entonces, dada la representación $h$ y el output $x$ (que este caso también es el input), podemos asumir que el output del decoder sigue una distribución $P_{decoder}(x|h)$. La función de pérdida es igual a la log-verosimilitud,  $-\log{P_{decoder}(x|h)}$, cuya forma funcional depende de los supuestos que hagamos sobre $P_{decoder}(x|h)$.

Podemos también generalizar esta idea al encoder, donde asumimos que su output tiene la siguiente distribución, $P_{encoder}(h|x)$.


***
# Tipos de Autoencoders
## Undercomplete Autoencoders

Como ya dijimos, aplicando restricciones durante el entrenamiento podemos lograr que el modelo capture información relevante sobre la distribución de los datos. En particular, si lo que queremos es obtener las features que más información aportan, tenemos que restringir $h$ para que tenga una menor dimensión que $x$. De esta manera lo que hacemos es forzar al modelo para que se concentre en las features más importantes para representar los patrones en los datos.

El proceso de aprendizaje es igual al de una red neuronal tradicional, y consiste en minimizar una **función de perdida**:
$$L(x, g(f(x)))$$
donde $L$ puede ser cualquier función que penalice al modelo cuando la reconstrucción es distinta al input $x$.
Un aspecto clave a considerar es que, si el encoder y el decoder son lineales y la función de pérdida es el error cuadrático medio (ECM), entonces el autoencoder aprende la misma **representación** que PCA. Sin embargo, la ventaja que tienen los autoencoders sobre PCA es que, si el encoder o el decoder (o ambos) son no lineales, incluso si usamos el ECM como función de pérdida, podemos capturar un espacio latente más complejo y no lineal.

Desafortunadamente, si no se imponen suficientes restricciones, incluso un autoencoder con un encoder y decoder no lineales puede aprender a reconstruir los datos sin capturar información relevante en el proceso.
En teoría, si no limitamos su capacidad, podría ocurrir que el encoder logre representar cada observación de la muestra de entrenamiento, $X$, con un índice $x^{(i)}$. En ese caso, el decoder solo tiene que aprender a mapear los índices $i$ con las observaciones $x^{(i)}$. Esto no ocurre en la práctica, pero es un buen ejemplo de como los autoencoders pueden aprender a realizar la tarea de pretexto sin aprender nada de la distribución de los datos.
## Regularized Autoencoders

Como mencionamos antes, si no se limita la capacidad del encoder y el decoder, el modelo puede aprender a reconstruir los datos sin extraer información útil. Idealmente, se podría entrenar exitosamente un autoencoder ajustando la capacidad del encoder y el decoder según la complejidad de la distribución a modelar.
Existen diversas técnicas de regularización que permiten entrenar autoencoders capaces de capturar información de la distribución sin tener que limitar la capacidad del encoder o decoder. Esto se logra modificando la función de pérdida para que el modelo adquiera propiedades adicionales, más allá de simplemente reconstruir los inputs.
Nuestro autoencoder puede ser no lineal y tener una representación de mayor dimensión que $x$, pero aún así puede aprender información relevante de la distribución, incluso sin limitar la capacidad del encoder o decoder.
### **Sparse Autoencoders**

Los **autoencoders esparsos** se utilizan para extraer features en problemas de clasificación. Para lograr que un autoencoder sea esparso, se agrega una penalización $\Omega$ sobre la representación $h$. La función de pérdida se define como:
$$L(x, g(f(x)))+\Omega(h)$$
Al imponer la penalización $\Omega$, evitamos que el autoencoder tenga un error de reconstrucción bajo en todo el espacio.
### **Denoising Autoencoders**

Un **denoising autoencoder (DAE)** es un autoencoder que recibe una versión perturbada de los datos, $\tilde{x}$, y a partir de ella intentar predecir la versión original. En otras palabras, la tarea de pretexto del autoencoder ya no es reconstruir el input $x$, sino quitarle el ruido a una versión perturbada, $\tilde{x}$.
![denoising-autoencoders](attachments/denoising-autoencoders.png)
Entrenarlo de esta manera fuerza a que el autoencoder aprenda de manera implícita la distribución $P(x)$ de los datos.
### **Contractive Autoencoders**

Los **contractive autoencoders (CAE)** se entrenan con una penalización $\Omega$ que penaliza la sensibilidad del espacio latente, $h=f(x)$, ante pequeños cambios en los inputs. Esta penalización utiliza la norma de Frobenius de la matriz Jacobiana (sencillamente, la suma de los cuadrados de los elementos de la matriz Jacobiana):
$$\Omega(h,x)=\lambda\sum_{i}||\nabla_{x}h_{i}||^{2}$$
donde $\nabla_{x}h_{i}=\frac{\partial h}{\partial x}$.
Al agregar esta penalización a la función de pérdida, obtenemos un autoencoder que, para aquellos puntos que se encuentran cerca en el espacio, también se van a encontrar cerca en el espacio latente.
Debido a que esta penalización solo se aplica a la muestra de entrenamiento, el modelo se ve forzado a ser insensible a cambios en $x$ dentro de las regiones donde existen datos de entrenamiento, pero no por fuera de ellas. Esto permite tener una mejor estimar un mejor espacio latente y obliga al modelo a aprender las características más informativas sobre la distribución $P(X)$.
***
# Resources
- \[1\] I. Goodfellow, Y. Bengio, and A. Courville, _Deep Learning_. Cambridge, MA: MIT Press, 2016. \[Online\]. Available: [http://www.deeplearningbook.org](http://www.deeplearningbook.org/).
- \[2\] J. Jordan, "Introduction to autoencoders.", *Jeremy Jordan*, 19 Mar 2018. \[Online\]. Available: [https://www.jeremyjordan.me/autoencoders/](https://www.jeremyjordan.me/autoencoders/).