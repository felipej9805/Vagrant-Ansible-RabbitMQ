#!/usr/bin/env python
import pika
import sys

#Las credenciales para conectarnos al servidor RabbitMQ
credentials = pika.PlainCredentials('root','password')

#Conexion con nuestro servidor RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.0.10', credentials=credentials))
channel = connection.channel()

channelBroadcast= connection.channel()


channel.exchange_declare(exchange='general', exchange_type='direct')

channelBroadcast.exchange_declare(exchange='broadcast', exchange_type='fanout')


result = channel.queue_declare(queue='estudiantes', exclusive=True)
queue_name = result.method.queue

resultBroadcast = channelBroadcast.queue_declare(queue='broadcast', exclusive=True)
queue_nameBroadcast = resultBroadcast.method.queue

channel.queue_bind(exchange='general', queue='estudiantes', routing_key='estudiantes')
channelBroadcast.queue_bind(exchange='broadcast', queue='broadcast', routing_key='')

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channelBroadcast.basic_consume(queue=queue_nameBroadcast, on_message_callback=callback, auto_ack=True)

channelBroadcast.start_consuming()
channel.start_consuming()
