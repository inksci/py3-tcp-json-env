# python 3

# 创建环境并定义维度参数
# create the env. and define its dimension parameters

import gym
env_name = "Pendulum-v0"
env = gym.make( env_name )

env.state_dim = env.observation_space.shape[0]
env.action_dim = env.action_space.shape[0]
env.DoF = 1

# 充当服务器的功能
# work as a servicer

import numpy as np
import socket
import threading
import json

TCP_PORT = 12005

def env_servicer(env):
    #Create The Socket
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #Listen The Port
    s.bind(('',TCP_PORT))
    s.listen(5)
    print('Waiting for connection...')

    def tcplink(sock,addr):
        print('Accept new connection from %s:%s...' % addr)
        sock.send( ('Welcome!').encode() )
        while True:
            data=sock.recv(1024).decode()
            print("data: ", data)

            data_json = json.loads( data )
            print('data_json["type"]: ', data_json["type"])

            if data_json["type"] == "init":
                data = { 'state_dim' : env.state_dim, 'action_dim' : env.action_dim, 'DoF' : env.DoF } 

            elif data_json["type"] == "reset":
                state = env.reset()
                data = { 'state' : state.tolist() } 

            elif data_json["type"] == "step":
                a = np.array( data_json["action"] )
                state_next, r, done, info = env.step(a)
                data = { 'state' : state_next.tolist(), 'reward' : r, 'done' : done, 'info' : info } 
            elif data_json["type"] == "close":
                break
                
            str_json = json.dumps(data)
            sock.send( str_json.encode() )
        sock.close()
        print('Connection from %s:%s closed.'%addr)
        
    while True:
        # Accept A New Connection
        sock,addr=s.accept()
        
        # Create A New Thread to Deal with The TCP Connection
        t=threading.Thread(target=tcplink(sock,addr))

env_servicer( env )