# -*- coding: utf-8 -*-

from socket import *

import pickle
import getpass

try:
    
    username = raw_input('Username: ')
    passwd = getpass.getpass('Password: ')

    sockobj = socket(AF_INET, SOCK_STREAM)

    sockobj.connect(('127.0.0.1', 3001)) # make a TCP/IP socket object
    sockobj.send(pickle.dumps({'what': 'auth', 'username': username, 'passwd': passwd}))
    
    data = sockobj.recv(1024)
    response = pickle.loads(data)
    
    sockobj.close()
  
    if response['status'] == 'ok':

        while True:
            prompt = raw_input('$ ').strip()
            
            sockobj = socket(AF_INET, SOCK_STREAM)
            sockobj.connect(('127.0.0.1', 3001)) # make a TCP/IP socket object
            sockobj.send(pickle.dumps({'what': 'oter', 'content': prompt}))
            
            data = sockobj.recv(1024)
            response = pickle.loads(data)
            
            if response['what'] == 'db_error':
                print 'Erro: ' + str(response['message'])
            elif response['what'] == 'db_cursor':
                for x in response['cursor']:
                    print x
            else:
                print 'OK'
            
    else:
        print 'Usuário e senha não combinam'

except KeyboardInterrupt:
    print 'Cliente encerrado\n'
except error, excp:
    print excp
    
