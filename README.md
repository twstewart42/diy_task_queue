<h1>Task Execution Queue</h1>


<h3>prerequisites</h3>
Install Python 2.7  

Install and Configure <a href="https://github.com/twstewart42/notes-wiki/tree/master/rabbitmq">RabbitMQ</a> on either a single node or a cluster of masters

<h3>How to use</h3>
<body>
Use:
In one window 
<pre>
  > git clone https://github.com/twstewart42/diy_task_queue.git
  > cd dir_task_queue/
  > python rpc_server_multi.py &
        [3] 3235196
         thread %(num)s
         thread %(num)s 
         thread %(num)s
         thread %(num)s
         [x] Awaiting RPC requests
         [x] Awaiting RPC requests
         [x] Awaiting RPC requests
         [x] Awaiting RPC requests
</pre>

Open 2nd window, or on differnet machine with access to same project files:
<pre>
  #git clone https://github.com/twstewart42/diy_task_queue.git
  #cd dir_task_queue/
  > python rpc_client.py -t "time ping -c 4 8.8.8.8"
  > python rpc_client.py -t "time ping -c 4 8.8.8.8" & python rpc_client2.py -t "time uname -a" & python rpc_client2.py -t "ti me sleep 6"
    [1] 3235320
    [2] 3235321
    [x] Requesting rpc
    [x] Requesting rpc
    [x] Requesting rpc
    [.] Got 'runtask.Tasker instance at 0x7f3e038757a0'
    [.] Got 'runtask.Tasker instance at 0x7f3e038757a0'
    [.] Got 'runtask.Tasker instance at 0x7f3e038757a0'
</pre>
Now back in the first window you should see all tasks run at the same time in parallel.
<pre>
 [x] Received 'time sleep 6'
 uuid '0f5fe5af-70eb-44af-a4e6-e5f479dfb88a':
0f5fe5af-70eb-44af-a4e6-e5f479dfb88a time sleep 6
 [x] Received 'time ping -c 4 8.8.8.8'
 uuid 'dfd19a5d-51ae-4411-9fa2-56fd6e6d3ca9':
dfd19a5d-51ae-4411-9fa2-56fd6e6d3ca9 time ping -c 4 8.8.8.8
 [x] Received 'time uname -a'
 uuid 'ed3370a0-ceab-4816-a69e-6a758be17daf':
ed3370a0-ceab-4816-a69e-6a758be17daf time uname -a

real    0m0.002s
user    0m0.000s
sys     0m0.001s
starting demotion #The demotion is set to force the task to run as a non-root user.
finished demotion
Linux bfezdxappa02.zedxinc.com 3.10.0-229.20.1.el7.x86_64 #1 SMP Tue Nov 3 19:10
None
 [x] Done

real    0m3.033s
user    0m0.000s
sys     0m0.002s
starting demotion
finished demotion
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=52 time=23.9 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=52 time=23.7 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=52 time=23.6 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=52 time=23.7 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 23.660/23.757/23.935/0.186 ms
None
 [x] Done

real    0m6.002s
user    0m0.001s
sys     0m0.000s
starting demotion
finished demotion
None
 [x] Done

</pre>
Will send three tasks at the same time to the rpc_server_multi to be executed.

One can start many rpc-server_multi porcesses on different machines, as long as they can communicate with the RabbitMQ service all messages should be recievable for both rpc_server and rpc_client.

I was building this to show a proof of concept, and I have sort of built a DIY version of Celery. I would recommend using Celery in production as there is a support and knowlegde base to work with, this was a very fun project to experiment with, and will hopefully act as a building block for much more robust Task execution queue.


</body>
