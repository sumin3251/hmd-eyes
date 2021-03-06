"""
Receive data from Pupil using ZMQ.
"""
import zmq
from msgpack import loads

context = zmq.Context()
# open a req port to talk to pupil
addr = '192.168.0.34'  # remote ip or localhost
req_port = "59502"  # same as in the pupil remote gui
req = context.socket(zmq.REQ)
req.connect("tcp://{}:{}".format(addr, req_port))

# ask for the sub port
req.send_string('SUB_PORT')
sub_port = req.recv_string()

# open a sub port to listen to pupil
sub = context.socket(zmq.SUB)
sub.connect("tcp://{}:{}".format(addr, sub_port))
print("Connected")

# set subscriptions to topics
# recv just pupil/gaze/notifications
#sub.setsockopt_string(zmq.SUBSCRIBE, 'pupil.')
sub.setsockopt_string(zmq.SUBSCRIBE, 'gaze')
# sub.setsockopt_string(zmq.SUBSCRIBE, 'notify.')
# sub.setsockopt_string(zmq.SUBSCRIBE, 'logging.')
# or everything:
# sub.setsockopt_string(zmq.SUBSCRIBE, '')


while True:
    try:
        print("s0")
        topic = sub.recv_string()
        print("1")
        msg = sub.recv()
        print("2")
        msg = loads(msg, encoding='utf-8')
        print("3")
        print("\n{}: {}".format(topic, msg))
    except KeyboardInterrupt:
        break
