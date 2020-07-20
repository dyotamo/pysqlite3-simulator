# -*- coding: utf-8 -*-

import pickle
import getpass
import socket

SERVER = '127.0.0.1'
PORT = 3000

try:
    username = input('Usuário: ')
    passwd = getpass.getpass('Senha: ')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER, PORT))
        sock.send(pickle.dumps(
            dict(what='auth', username=username, passwd=passwd)))

        data = sock.recv(1024)
        response = pickle.loads(data)

        if response['status'] == 'ok':
            while True:
                prompt = input('$ ').strip()

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((SERVER, PORT))
                sock.send(pickle.dumps(dict(what='oter', content=prompt)))

                data = sock.recv(1024)
                response = pickle.loads(data)

                if response['what'] == 'db_error':
                    print('Erro: {}'.format(response['message']))
                elif response['what'] == 'db_cursor':
                    for line in response['cursor']:
                        print(line)
                else:
                    print('OK')
        else:
            print('Usuário e senha não combinam')
except KeyboardInterrupt:
    print('Cliente encerrado')
