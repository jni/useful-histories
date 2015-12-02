# IPython log file


import zmq
comm = zmq.Context().socket(zmq.PAIR)
comm.connect('tcp://localhost:5556')
msg_sep = {'type':'separate', 'data': {'segments': [3, 4]}}
msg_mrg = {'type':'merge', 'data': {'segments': [1, 2, 3]}}
msg_lut = {'type':'request', 'data': {'what': 'fragment-segment-lut'}}
msg_stop = {'type': 'stop', 'data': {}}
comm.send_json(msg_sep)
comm.send_json(msg_mrg)
comm.send_json(msg_lut)
comm.send_json(msg_stop)
comm.recv_json()
