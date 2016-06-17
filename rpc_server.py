#!/usr/bin/env python
#################
#
# rpc_server.py written to listen for messages in the queue
# Author: Tom Stewart
# You have my permission to use this in any way. Open Source
#
###################



import pika
from runtask import Tasker

credentails = pika.PlainCredentials('execute', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='rbt001', port=5672, credentials=credentails, virtual_host='test'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
	if n == 0:
		return 0
	elif n == 1:
		return 1
	else:
		return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
	#n = int(body)

	if body == 'fib':
		n = sum(c != ' ' for c in body)
		print(" [.] fib(%s)" % n)
		
		response = fib(n)
	else:
		print " [x] Received %r" % (body,)
		print " uuid %r: " % (props.correlation_id,)
                #task1 = Tasker(12345, "ping -c 4 8.8.8.8")
                #task1.task_do()
                response = Tasker(props.correlation_id, body)
                response.task_do()
                print(" [x] Done")

	ch.basic_publish(exchange='',routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = \
          props.correlation_id),body=str(response))
	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
