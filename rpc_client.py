#!/usr/bin/env python
#################
#
# rpc_client.py written to submit new tasks into the queue
# Author: Tom Stewart
# You have my permission to use this in any way. Open Source
#
###################
import pika
import uuid
import sys
import argparse

class RpcClient(object):
    def __init__(self):
	credentails = pika.PlainCredentials('execute', 'password')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                 host='rbt001', port=5672, credentials=credentails, virtual_host='test'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n, uid):
        self.response = None
        self.corr_id = uid
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def main():
	
	parser = argparse.ArgumentParser(description="Submits task with UID")
	parser.add_argument('-u', dest='uid', type=str, help='Unique Identifier for task')
	parser.add_argument('-t', dest='task', type=str, help='Task to be ran')
	args = parser.parse_args()

	if args.uid is None:
		uid = str(uuid.uuid4()) 
	else:
		uid = args.uid

	if args.task is None:
		message = "echo Hello World"
	else:
		message = args.task
	#essage = ' '.join(sys.argv[1:]) or "Hello World!"
	rpc = RpcClient()

	print(" [x] Requesting rpc")
	response = rpc.call(message, uid)
	print(" [.] Got %r" % response)

if __name__ == '__main__':
	main()

