<h1>Task Execution queue</h1>


<h3>Prequistie</h3>
Install RabbitMQ on either a single node or a cluster of masters

<h3>How to use</h3>
<body>
Use:
In one window 'python rpc_server_multi.py &'

In 2nd window, or differnet machine:
python rpc_client2.py -t "time ping -c 4 8.8.8.8" & python rpc_client2.py -t "time uname -a" & python rpc_client2.py -t "ti me sleep 6"

Will send three tasks at the same time to the rpc_server_multi to be executed.

One can start many rpc-server_multi porcesses on different machines, as long as they can communicate with the RabbitMQ service all messages should be recievable for both rpc_server and rpc_client.

I was building this to show a proof of concept, and I have sort of built a DIY version of Celery. I would recommend using Celery in production as there is a support and knowlegde base to work with, this was a very fun project to experiment with, and will hopefully act as a building block for much more robust Task execution queue.


</body>
