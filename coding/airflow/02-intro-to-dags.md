***
Un DAG (Directed Acyclic Graph) es un modelo que contiene toda la información necesaria para poder ejecutar nuestros trabajos.
Algunos de sus atributos son:
- **Schedule.** Define cuando se debe ejecutar el flujo de trabajo.
- **Tasks.** Define cuales son las tareas que definen nuestro flujo de trabajo.
- **Dependencies.** El orden en que se deben ejecutar las tareas, y bajo que condiciones.
- **Callbacks.** Acciones que se deben tomar una vez completado el flujo de trabajo.

# 🔨 Crear un DAG

Hay tres formas de crear un DAG[^1]. La primera opción es usar el comando `with` (context manager) de Python:
```python
import datetime
from airflow.models.dag import DAG
from airflow.providers.standatd.operators.empty import EmptyOperator

with DAG(
	dag_id='dag-name',
	description='My first DAG.',
	start_date=datetime.datetime(2025,5,2),
	schedule='@daily'
):
	EmptyOperator(task_id='task')
```

La segunda es crear una instancia de la clase `DAG`, y luego pasar esa instancia a los operadores:
```python
import datetime
from airflow.models.dag import DAG
from airflow.providers.standatd.operators.empty import EmptyOperator

my_dag = DAG(
	dag_id='dag-name',
	description='My first DAG.',
	start_date=datetime.datetime(2025,5,2),
	schedule='@daily'
)
EmptyOperator(task_id='task', dag=my_dag)
```

La última opción es usar un decorator, `@dag`, que transforma una función en un DAG:
```python
import datetime
from airflow.models.dag import DAG
from airflow.providers.standatd.operators.empty import EmptyOperator

@dag(
	dag_id='dag-name',
	description='My first DAG.',
	start_date=datetime.datetime(2025,5,2), 
	schedule='@daily'
)
def generate_dag():
	EmptyOperator(task_id='task')

generate_dag()
```

## 🏃🏼 DAG Run



# 🔨 Crear una tarea

Las tareas son la unidad básica de ejecución en Airflow. Cada tarea tiene una dependencia, ya sea porque depende de la ejecución de una tarea para poder ejecutarse (se conoce como *upstream dependency*) o porque hay otras tareas que dependen de su ejecución para poder ser ejecutadas (se conoce como *downstream dependency*).
Hay tres tipos básicos de tareas:
- **Operators.** Son tareas predefinidas que podemos utilizar en nuestro DAG[^2]. Algunos de los operators más comunes son:
	- `BashOperator`. Nos permite ejecutar comandos en la terminal.
	- `PythonOperator`. Nos permite ejecutar una función de Python arbitraria.
- **Sensors.** Son un tipo de Operators que se ejecutan cuando un evento ocurre, y no se ejecutan si ese evento no ocurre.
- **TaskFlow.** Son funciones de Python que pueden ser utilizadas como tareas. 

### ⛓️ Dependencias

Como dijimos anteriormente, la parte más importante al trabajar con tareas es poder definir relaciones (dependencias) entre ellas.
Hay dos maneras de declarar las dependencias entre tareas:
- La primera es usar `<<` y `>>`. En el siguiente ejemplo le estamos especificando al DAG que la segunda tarea depende de la primera para ser ejecutada, y que la tercera y la cuarta tarea se van a ejecutar en simultáneo una vez ejecutada la segunda.
```python
first_task >> second_task >> [third_task, fourth_task]
```
- La segunda forma es utilizar los métodos `set_upstream()` y `set_downstream()`. Esta forma es más explícita, pero en algunos casos es más difícil de entender.
```python
first_task.set_downstream(second_task)
second_task.set_downstream([third_task, fourth_task])
```

Algo importante a tener en cuenta es que, por defecto, las tareas se ejecutan de manera aislada y no se transfieren información entre ellas. Si quisiéramos transferir información entre las tareas, deberíamos utilizar `XComs`.

[^1]: Para más información sobre la clase `airflow.models.dag.DAG` ir a la [documentación oficial](https://airflow.apache.org/docs/apache-airflow/2.1.1/_api/airflow/models/dag/index.html).
[^2]: La mayoría de las veces vamos a utilizar los términos Tasks y Operator como sinónimos. Sin embargo, ambos representan dos objetos distintos: un Task es la unidad genérica de ejecución en un DAG, mientras que un Operator es una "plantilla" de un Task.