#!/usr/bin/env python
import pika
import sys

#Las credenciales para conectarnos al servidor RabbitMQ
credentials = pika.PlainCredentials('root','password')

#Conexion con nuestro servidor RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.0.10', credentials=credentials))
channel = connection.channel()

#Declaramos el exchange
channel.exchange_declare(exchange='topic-messages', exchange_type='topic')

#Routing_key sera lo que nos permitira indicar hacia que grupo de consumidor ira el mensaje, y tambien se ingresara por consola
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'

#Mensaje que vamos a enviar el cual sera ingresado por consola, y por defecto enviara "Hola a todos"
message = ' '.join(sys.argv[2:]) or 'Hola a todos'

channel.basic_publish(exchange='topic-messages', routing_key=routing_key, body=message)

print(" [x] Enviado %r:%r" % (routing_key, message))

#Cerramos la conexion
connection.close()
