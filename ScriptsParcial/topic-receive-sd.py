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

#Declaramos la cola, y la etiqueta exclusive, nos indica
#que una vez la conexion del consumidor se cierra, la cola 
#sera eliminada
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

#El binding_key nos permite decirle al exchange que envie los mensajes
#a nuestra cola
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic-messages', queue=queue_name, routing_key=binding_key)

print(' [*] Esperando mensajes. Para salir presione CTRL +C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()