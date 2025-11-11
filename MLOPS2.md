# Repositorio de GitHub (50% de la unidad)

Considerando el mismo problema descrito en la anterior unidad (predicción de una enfermedad en pacientes), una vez se ha desarrollado la solución local para el médico, se necesita ahora definir y estructurar un repositorio en GitHub para mantener un correcto control sobre la solución. Para esto, necesitan realizar los siguientes pasos:

1.	Crear un repositorio en GitHub con la siguiente forma: “<nombre>-mlops-U2”. El nombre lo eligen ustedes. Deben agregar mi usuario (aviladavid28@gmail.com) como Colaborador (Settings -> Collaborators & Teams).

2.	La rama principal (main) debe contener inicialmente un md en donde se explique el problema, el propósito y la estructura del repositorio, y cualquier otro detalle que consideren importante. No tiene que ser muy extenso. Este archivo debe usar el lenguaje Markdown, ampliamente usado en estos repositorios.

3.	Crear una primera rama llamada solución-inicial en donde se agreguen todos los archivos propuestos en la unidad 1, excepto el archivo con el pipeline propuesto del proceso en general. Estos deben agregarse tal cual fueron presentados, no importa si quizás tienen algún error lógico o funcional. El archivo md que crearon en el punto anterior debe actualizarse con el README que presentaron en la semana 2; no deben existir dos READMEs distintos. Todo esto se debe realizar en un solo commit.

4.	Crear un PR (pull request) para agregar los cambios de esta rama a la rama principal. No deben agregar ningún reviewer, solo deben crear el PR y luego hacer un merge a la rama principal.

5.	Una vez la rama main esté actualizada con la solución inicial, pueden crear una segunda rama llamada segunda-versión en donde agreguen cualquier cambio que crean necesario. Es decir, esta rama es necesaria para aquellas personas que hayan recibido algún comentario en la semana 2 respecto a cambios que deban considerar; si no recibieron ningún comentario respecto a algo por cambiar, pueden saltarse este paso. Una vez hayan agregado los cambios, deben hacer otro PR y luego el respectivo merge a la rama principal.

6.	Consideren ahora estos nuevos requerimientos:

    - Nueva predicción: Los médicos necesitan agregar una nueva categoría a las predicciones del modelo que se llame ENFERMEDAD TERMINAL. Es decir, se necesitan ahora 5 categorías en total como respuestas del modelo. En una solución real, esto implicaría reentrenar el modelo para tener una nueva categoría. En nuestro ejercicio simplificado, basta con agregar algunas nuevas líneas en la función que simula las predicciones.
    - Nueva funcionalidad: Los médicos necesitan obtener un reporte con algunas estadísticas de las predicciones realizadas. En concreto, necesitan saber:
        - Número total de predicciones realizadas por cada categoría.
        - Últimas 5 predicciones realizadas.
        - Fecha de la última predicción.

    Para lograr esto, bastaría con exportar algunos resultados por cada predicción que se realice. Pueden exportarse en algún archivo de texto que luego pueda ser leído y retornado a los médicos que lo necesiten. Es decir, se necesita agregar una nueva forma de obtener estos resultados a través de la forma que hayan escogido para realizar el despliegue a través de Docker.

    Se necesitan desarrollar los anteriores requerimientos y agregarlos a la rama principal. Esto lo deben hacer a través de ramas, pueden ser dos (una para cada requerimiento) o, si lo hacen en una única rama, deben existir al menos dos commits distintos que muestren explícitamente los cambios para cada requerimiento. Una vez estén listos los cambios, deben hacer los respectivos PRs (uno o dos dependiendo del número de ramas que hayan decidido), no necesitan ningún reviewer, y luego hacer el merge a la rama principal.

7.	That’s it! Los médicos tienen la solución final con los nuevos requerimientos.
 
# CI/CD a través de GitHub Actions (50% de la unidad)

Una vez se ha desarrollado la solución local para el médico y se han añadido todos los nuevos requerimientos, se necesita ahora definir y estructurar un pipeline de CI/CD para el repositorio en donde está alojado el proyecto a través de GitHub Actions. Para esto, deben crear una nueva rama llamada añadir-github-actions y realizar todo el desarrollo allí.

Como buena práctica en general para repositorios, la rama principal puede estar protegida y esto implica que solo se pueden agregar cambios a esta a través de pull requests. Esto evita que existan cambios indeseados en la rama principal y ayuda a que los cambios tengan que al menos ser revisados o se realicen a través de un flujo definido. Así puede tenerse mayor trazabilidad en ellos. Antes de desarrollar el workflow con GitHub Actions, debe proteger la rama principal y aquí encuentran un link. con la información detallada de cómo hacerlo. Esto es importante para que los eventos y las tareas a definir tengan sentido (respecto a ser buenas prácticas de integración y desarrollo) y para que el repositorio sea similar al que se tendría para un modelo real en producción.

Para este pipeline deben existir dos eventos principales:

1.	Un evento que referencie cada PR realizado contra la rama main
2.	Un evento que referencie cada commit realizado en la rama main
 
Para el evento (1.), referencia a cada PR realizado contra la rama main se deben realizar las siguientes tareas:

1.	Se debe comentar en el PR el siguiente mensaje: “CI/CD en acción. Ejecutando tareas …”. Este mensaje es para indicarle al creador del PR y los usuarios involucrados que el pipeline ha comenzado. Pueden guiarse y usar esta acción.
2.	Se deben realizar unas pruebas unitarias en el nuevo modelo desarrollado. Es decir, esta tarea debe correr alguna instrucción sobre el repositorio que se encargue de correr al menos DOS pruebas unitarias. Las pruebas unitarias pueden ser algo como:

    - Dados unos parámetros de entrada, probar que la respuesta del modelo es algún tipo de enfermedad esperado. Por ejemplo, si el paciente tiene 20 años, síntomas leves respiratorios y alguna condición neurológica, se espera que la respuesta sea ENFERMEDAD LEVE.
    - Realizar una predicción que arroje algún tipo de enfermedad, y luego chequear las estadísticas (a través de la forma que hayan definido en la semana anterior, ya sea por revisar el archivo directamente, hacer una petición a la forma de despliegue, entre otros) para asegurarse que la última predicción realizada sea la esperada.
    - Antes de correr cualquier predicción, pedir las estadísticas y esperar que estas se encuentren vacías o con los valores por defecto que se hayan definido.
    - Considerar distintos grupos de parámetros de entrada al modelo y esperar que las 5 categorías de enfermedades sean obtenidas.

Hay muchas pruebas que se pueden realizar tanto en las funcionalidades como en la estructura del repositorio para asegurarse que todos los nuevos cambios están bien codificados, sin embargo, para este ejercicio basta con realizar solo dos pruebas a modo de prueba. Para correr pruebas unitarias en Python pueden usar una librería como pytest, o pueden usar cualquier otra libraría de tests (o una forma propia de pruebas también) en el lenguaje que estén usando.

Finalmente, las pruebas las pueden correr directamente en el repositorio (GitHub Actions corre las pruebas sobre un entorno en Ubuntu por ejemplo) o pueden construir la imagen de Docker que hayan definido en el repo (usando el Dockerfile que hayan escrito) y correr las pruebas allí; todo esto se define en el archivo workflow.yaml. En este link encuentran algunas referencias sobre cómo realizar estas pruebas.

3.	Una vez las pruebas hayan terminado, se debe comentar en el PR el siguiente mensaje: “CI/CD terminado con éxito.”. Este mensaje es para indicarle al creador del PR y los usuarios involucrados que todo está correcto y el PR está listo para la revisión final.
 
Para el evento (2.), referencia a cada commit realizado en la rama main (es decir, después de cada merge o cada push a través de PRs ya que la rama está protegida contra commits directos) se deben realizar las siguientes tareas:

1.	Se deben volver a correr las pruebas unitarias definidas para el evento anterior. Bastaría con volver a hacer un llamado a que se ejecuten las pruebas. Esto se hace como una verificación final a que el código, ya existente en main, no tiene ningún error funcional o lógico.

2.	Se debe construir la nueva imagen de Docker, con todos los nuevos cambios, y se debe publicar en el registro de paquetes de GitHub. Esto se puede considerar como una forma final de despliegue en donde la imagen va a ser publicada en un repositorio de imágenes para luego poder ser utilizada, llamada o invocada desde cualquier otro servicio. GitHub Packages es gratuito para repositorios privados con algunas limitaciones de almacenamiento, sin embargo, esta cuenta gratuita es más que suficiente para la imagen a construir en este proyecto. Pueden guiarse y usar esta acción.
 
Como se mencionó anteriormente, estos cambios los deben realizar en una rama llamada añadir-github-actions y, una vez tengan todos los cambios necesarios allí, deben realizar un PR a main y luego hacer un merge. Así, la rama main estará actualizada con todos los nuevos cambios.

Las referencias acá mostradas respecto a acciones ya definidas provienen del Marketplace de GitHub Actions. Estas son tareas que han sido definidas por otros usuarios, y al ser tareas comunes que muchos creadores de código pueden encontrar útiles, los usuarios deciden agregarlas al Marketplace para que puedan ser usadas por cualquier persona. Estas acciones son agregadas al Marketplace con algún indicador único, y pueden ser invocadas desde cualquier pipeline y repositorio. No tienen que usar las acciones referenciadas en los puntos anteriores, ustedes pueden definir sus propias acciones desde cero sin mucha complejidad para las tareas acá propuestas. Puede ser una buena forma de practicar código desde cero y así entender más a profundidad la razón de ser de GitHub Actions.
