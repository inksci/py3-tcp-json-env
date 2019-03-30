# python 3

import numpy as np
import socket
import json

TCP_PORT = 12005

# 充当客户端的角色
# act as a client

class tcp_env():
    def __init__(self, tcp_port):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.s.connect(('127.0.0.1',tcp_port))

        print( self.s.recv(1024).decode())

        data = { 'type' : 'init' } 

        str_json = json.dumps(data)
        self.s.send( str_json.encode() )
        str_recv = self.s.recv(1024).decode()
        
        data_json = json.loads( str_recv )
        
        self.state_dim = data_json["state_dim"]
        self.action_dim = data_json["action_dim"]
        self.DoF = data_json["DoF"]

        # s.send('exit')
        # s.close()        
        
    def  reset(self):
        data = { 'type' : 'reset' } 

        str_json = json.dumps(data)
        self.s.send( str_json.encode() )
        str_recv = self.s.recv(1024).decode()
        
        data_json = json.loads( str_recv )
        
        state = np.array( data_json["state"] )
        return state
    def step(self, action):
        
        data = { 'type' : 'step', 'action' : action.tolist() } 

        str_json = json.dumps(data)
        self.s.send( str_json.encode() )
        str_recv = self.s.recv(1024).decode()
        
        data_json = json.loads( str_recv )
        
        state = np.array( data_json["state"] )
        r = data_json["reward"]
        d = data_json["done"]
        info = data_json["info"]
        
        return state, r, d, info
    def close_tcp(self):
        print(" close tcp ... ")
        data = { 'type' : 'close' } 

        str_json = json.dumps(data)
        self.s.send( str_json.encode() )
        self.s.close()        
env = tcp_env( tcp_port = TCP_PORT )

# 测试
# test

env.reset()

env.step( np.array( [0.1] ) )

env.close_tcp()