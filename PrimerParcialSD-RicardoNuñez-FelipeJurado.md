## Primer Parcial Sistemas Distribuidos 2020-1
#### Felipe Jurado A00328420
#### Ricardo Nuñez A00030132

##### Arquitectura del problema
- Tenemos un productor de mensajes
- Un broker de RabbitMQ (Máquina física)
- Dos consumidores de mensajes(Máquinas virtuales)

-El primero serán los estudiantes

-El segundo serán los profesores

Se comenzó revisando cada uno de los ejemplos de RabbitMQ, con el objetivo de entender en su totalidad cada uno de ellos, para posteriormente lograr adaptar y mezclar los que consideramos más pertinentes para el parcial y se procedió a hacer la ejecución de manera local.

Es decir, se instaló el broker RabbitMQ en la máquina física, y se procedió a ejecutar los respectivos scripts de python, en dónde la conexión se lleva a cabo por medio de localhost. Las líneas exactas de dicha conexión se muestran en la imagen 1, en dónde se crea la conexión con el parámetro del host como localhost. 

El objetivo de hacer este procedimiento primero de manera local, es para lograr entender y tener todo un poco más controlado para su implementación y posteriormente lograr llevarlo a un sistema distribuido haciendo uso de Vagrant para la creación de las máquinas y Ansible para su respectivo aprovisionamiento. Las evidencias de la correcta ejecución de los archivos de manera local se encuentran en la imagen 2.

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/conexionLocalhost.png">

Imagen 1: Conexión de manera local

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/ejecucionScriptsLocalhost.png">

Imagen 2: Evidencia de la ejecución de los scripts de manera local

### 2. Documentación del procedimiento para el aprovisionamiento del productor (10%). Evidencias del funcionamiento (5%).

Para el aprovisionamiento del productor, por medio de un Vagrant File, se hizo la respectiva creación de la máquina virtual en donde se configuran parámetros como la dirección IP, memoria y el puerto ssh de la máquina. Adicionalmente, la máquina virtual del productor, al igual que el resto de las máquinas, se crean con sistema operativo ubuntu-19.10, y en dónde finalmente se indica que el aprovisionamiento se realizará por medio de ansible, y dicho archivo se encuentran en la carpeta playbooks y el archivo es server.yml. A continuación se muestra la configuración del vagrant file:

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/vagrantFile.png">

Imagen 3: Archivo Vagrant File.

Por otro lado, en el archivo servers.yml, se encuentran las tres secciones de los tres diferentes hosts, es decir, el productor y los dos consumidores.

Puntualmente en la **sección de aprovisionamiento del productor**, aunque tienen muchas líneas similares con las secciones de los consumidores, primeramente se crea una carpeta en la máquina virtual del productor, en donde posteriormente se descargan los scripts desde un repositorio de Github que luego se ejecutarán..

También se **instala Git**, y seguidamente se encuentran las líneas para **clonar el repositorio** donde se encuentran los scripts y se guardarán en la carpeta previamente creada y finalmente están las líneas de aprovisionamiento para **instalar pip y el módulo de pika**, los cuales son necesarios para ejecutar los scripts de python.

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/aprovisionamientoProducerParte1.png">


Imagen 4: Aprovisionamiento del productor


Para intentar de alguna manera automatizar la ejecución de los scripts y por lo tanto el envío de los respectivos mensajes, hemos decidido crear 5 scripts los cuales son:
- **producer-estudiantes.py**
- **producer-profesores.py**
- **receiver-estudiantes.py**
- **receiver-profesores.py**
- **broadcast.py**

En el productor se ejecutan ambos archivos producer(estudiantes y profesores) y el archivo broadcast. 

El **producer.estudiantes.py** se encarga de enviar el mensaje hacia los estudiantes y el cual se crea un exchange y posteriormente se envía el mensaje con un routing:key llamado “estudiantes”, el cual debe ser el mismo en los consumidores para lograr que los mensajes lleguen correctamente. 

De manera similar es el **producer.profesores.py**, pero en este caso cambiaría el routing_key por “profesores”. Y por último el script de **broadcast.py**, es el encargado de enviar el mensaje tanto a los estudiantes como a los profesores por medio de un exchange tipo ‘fanout’, mientras que los dos producer anteriores, son de tipo ‘direct’.

Volviendo a nuestro archivo servers.yml, en la sección del productor, se deben ejecutar dos comandos por cada uno de los tres scripts que deben ser ejecutados en el productor. La primera línea del aprovisionamiento se encarga de dar permisos de ejecución al script y la segunda se encarga de ejecutar el respectivo script.

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/aprovisionamientoProducerParte2.png">


Imagen 5: Aprovisionamiento del productor

### 3. Documentación del procedimiento para el aprovisionamiento de los consumidores (10%). Evidencias del funcionamiento (5%).

Para el aprovisionamiento de cada uno de **los consumidores**, que en nuestro caso serán **los profesores(ConsumerA) y estudiantes(ConsumerB)**, se hizo la creación de las maquinas por medio del vagrant file presentado en la imagen 3 en la sección anterior, con las mismas características del productor.

Puntualmente en la **sección de aprovisionamiento de cada uno de los consumidores**, se crea la carpeta, se instala git, se clona el repositorio con los scripts y se instalan los módulos de pip y pika.

En **los consumidores** se ejecutan los archivos receiver en los profesores y estudiantes respectivamente, los cuales se encargan de estar escuchando y recibiendo los mensajes que serán enviados por el productor por las respectivas colas creadas en los scripts. Adicionalmente se debe agregar líneas en el script para permitir también la recepción de los mensajes enviados por el script broadcast ejecutado desde el productor. A continuación se muestra el aprovisionamiento tanto del ConsumerA (Profesores) y ConsumerB (Estudiantes):

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/aprovisionamientoConsumerProfesor.png">


Imagen 6: Aprovisionamiento para la automatizacion de los script de los profesores


<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/aprovisionamientoConsumerEstudiantes.png">


Imagen 7: Aprovisionamiento para la automatizacion de los script de los estudiantes


A continuación se muestran las evidencias de la recepción de los mensajes en cada uno de los consumidores:

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/evidencia-envioMensajes.png">


Imagen 8: Evidencia del correcto aprovisionamiento del productor y consumidores.

### 4. Documentación del procedimiento para el aprovisionamiento del broker (10%). Evidencias del funcionamiento (5%).

Para el Broker, hemos decidido utilizar una máquina física con Ubuntu 19.04, en dónde se realizó la instalación del servidor RabbitMQ, el cual será el servidor que se encarga de manejar la recepcion y envio de los mensajes entre el productor y los consumidores, adicionalmente permite crear las respectivas colas para cada uno de los consumidores

Para su instalación se siguio la siguiente guía encontrada: 

(https://computingforgeeks.com/how-to-install-latest-rabbitmq-server-on-ubuntu-18-04-lts/) 

En resumen, el proceso de instalación se ejecutan los siguientes comandos (todo el proceso debe realizarse con usuario root):

`` apt-get update `` Instalar actualizaciones en el sistema 

##### Paso 1: Instalación Erlang/OTP
Erlang es un lenguaje de programación funcional, de propósito general, concurrente y un entorno de tiempo de ejecución.

```wget -O- https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc | sudo apt-key add - ```

``` echo "deb https://packages.erlang-solutions.com/ubuntu bionic contrib" | sudo tee /etc/apt/sources.list.d/rabbitmq.list ```

``` sudo apt update ```

``` sudo apt -y install erlang ```

#### Pasó 2: Adicionar el repositorio de RabbitMQ

RabbitMQ es un software de agente de mensajes de código abierto que implementa el Protocolo avanzado de mensajes en cola (AMQP) y el Protocolo de mensajes orientados a la transmisión de mensajes de texto, el Transporte de telemetría de mensajes en cola y otros protocolos a través de complementos.

``` wget -O- https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc | sudo apt-key add - ```

``` wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add - ```

``` echo "deb https://dl.bintray.com/rabbitmq/debian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/rabbitmq.list ```

``` sudo apt update ```

``` sudo apt -y install rabbitmq-server ```

Ahora podemos comprobar que se encuentran correctamente instalado con los siguientes comandos:

``` systemctl is-enabled rabbitmq-server.service ```
``` systemctl status rabbitmq-server.service``` 

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/validacionInstalacionBroker.png">


Imagen 9: Aprovisionamiento para la automatizacion de los script de los estudiantes

### 7. Documente algunos de los problemas encontrados y las acciones efectuadas para su solución al aprovisionar la infraestructura y aplicaciones (10%).

#### Problemas

En la ejecución de los scripts, cuando se realizaban después de hacerlo en la máquina física, y posteriormente se ejecutaban en las máquinas creadas, apareció el siguiente error:

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/problema1_LoginRefused.png">


Imagen 10: Error LoginRefused

El error nos indicaba que la conexión de pika con el servidor RabbitMQ había sido rechazada e investigando nos dimos cuenta que por defecto el intenta siempre con el usuario guest, pero este solo funciona cuando se encuentran en localhost. Por este motivo era necesario crear las credenciales para conectarnos, en dónde se indicará el usuario y la clave de nuestro servidor RabbitMQ, que en nuestro caso sería nuestra máquina física y posteriormente esta variable se le pasará como parámetro en la conexión de pika con el servidor. 

Está modificacion se debio realizar tanto en el productor como en los consumidores para que ambos lograran tener comunicación con el servidor. La modificación de los scripts se encuentran en las primeras líneas de los scripts como se muestra a continuación: 

<img src="https://github.com/felipej9805/Vagrant-Ansible-RabbitMQ/blob/master/imagenes/problema1_solucion.png">


Imagen 11:  Solucion al error LoginRefused

Adicionalmente a esto,se debe agregar las siguientes líneas en nuestra máquina física para crear el usuario, se asigna como administrador y se le dan los permisos, esto se realiza con los siguientes comandos:

``` sudo rabbitmqctl add_user {username} {password} ``` Creamos un usuario


``` sudo rabbitmqctl set_permissions -p / {username} ".*" ".*" ".*" ``` Cambiamos los permisos al usuario


``` sudo service rabbitmq-server restart ``` Finalmente, reiniciamos el servidor rabbitmq.

Y finalmente con este proceso, se logró la conexión con el servidor RabbitMQ tanto en el productor como en los consumidores.

### Conclusiones
1. Realizar la implementación de la gestión de mensajeria utilizando RabbitMQ  fue bastante sencillo y practico, cumpliendo con los objetivos de manera efectiva, ya que la pagina web de RabbitMQ cuenta con una alta documentación clara para el seguimiento y puesta en marcha del servidor.

2. Se logro evidenciar el potencial del uso de herramientas como Vagrant y Ansible para la creación y aprovisionamiento de maquinas virtuales respectivamente, las cuales fueron herramientas bastante utiles para el desarrollo del parcial, y claramente para posteriores usos en la vida practica laboral.

3. Con respecto a Python tambien nos dimos cuenta, que apesar de que no se tiene mucho conocimiento, es bastante practico y sencillo cuando se comienzo a trabajar con dicho lenguaje de programación, ademas el gran uso que se le esta dando actualmente en la industria, es de vital importancia comenzar a conocer dicho lenguaje de programación

### Referencias

Autenticación pika : https://stackoverflow.com/questions/26811924/spring-amqp-rabbitmq-3-3-5-access-refused-login-was-refused-using-authentica 

Instalación RabbitMQ: https://computingforgeeks.com/how-to-install-latest-rabbitmq-server-on-ubuntu-18-04-lts/

Instación Pika: https://zoomadmin.com/HowToInstall/UbuntuPackage/python-pika

Documentación RabbitMQ: https://www.rabbitmq.com/getstarted.html
