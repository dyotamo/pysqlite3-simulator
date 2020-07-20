import sqlite3
import pickle
import socket

from datetime import datetime

SERVER = '0.0.0.0'
PORT = 3000


with open('migrate.sql', 'r') as f:
    c = sqlite3.connect('db/database')
    c.execute(f.read())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((SERVER, PORT))
sock.listen(15)

print('Servidor ouvindo na porta {} ...'.format(PORT))

while True:
    try:
        connection, address = sock.accept()
        print('Conexão de {}, às {}'.format(address, datetime.now()))

        data = connection.recv(1024)
        request = pickle.loads(data)

        print('Tipo: {}'.format(request['what']))

        if request['what'] == 'auth':
            cur = c.cursor()
            cur.execute('SELECT count(*) FROM user WHERE username = ? AND passwd = ?',
                        (request['username'], request['passwd'],))
            if cur.fetchall()[0][0] == 1:
                connection.send(pickle.dumps(dict(status='ok')))
            else:
                connection.send(pickle.dumps(dict(status='mismatch')))
        else:
            try:
                s = request['content'].lower()
                if s.startswith('select'):
                    cur = c.cursor()
                    result_set = [i for i in cur.execute(s)]
                    connection.send(pickle.dumps(
                        dict(what='db_cursor', cursor=result_set)))
                else:
                    c.execute(s)
                    connection.send(pickle.dumps(dict(what='db_ok')))
            except sqlite3.Error as a:
                connection.send(pickle.dumps(
                    dict(what='db_error', message=a)))
    except KeyboardInterrupt:
        print('Servidor encerrado')
        break
