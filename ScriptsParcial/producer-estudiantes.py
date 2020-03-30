#!/usr/bin/env python
import pika
import sys
#Las credenciales para conectarnos al servidor RabbitMQ
credentials = pika.PlainCredentials('root','password')

#Conexion con nuestro servidor RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.0.10', credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='general', exchange_type='direct')

message = 'Hello Students!!'

channel.basic_publish(
    exchange='general', routing_key='estudiantes', body=message)
print(" [x] Sent %r" % (message))
connection.close()