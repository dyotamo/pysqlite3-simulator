# -*- coding: utf-8 -*-

from socket import *
from datetime import datetime

import sqlite3
import pickle   

import hashlib     

if __name__ == '__main__':
    
    c = sqlite3.connect('db/database')
    c.execute('CREATE TABLE IF NOT EXISTS user(username varchar(35) PRIMARY KEY, passwd VARCHAR(35))')
    
    sockobj = socket(AF_INET, SOCK_STREAM)

    sockobj.bind(('', 3000))
    sockobj.listen(5) # 5 é um bom número ...

    print 'Servidor ouvindo na porta 3000 ...'

    while True:
        try:
            connection, address = sockobj.accept()
            data = connection.recv(1024)

            print 'Conexão de %s, às %s' % (address, str(datetime.now()))
            request = pickle.loads(data)
            
            print 'Tipo: ' + request['what']
            
            if request['what'] == 'auth':
                cur = c.cursor()
                cur.execute('SELECT Count(*) FROM user WHERE username = ? AND passwd = ?', (request['username'], request['passwd'],))
              
                if cur.fetchall()[0][0] == 1: # Resultcount ...
                    connection.send(pickle.dumps({'status': 'ok'}))
                else:
                    connection.send(pickle.dumps({'status': 'mismatch'}))
            else:
                try:
                    s = request['content'].lower()
                    
                    if s.startswith('select'):
                        cur = c.cursor()
                        result_set = [i for i in cur.execute(s)]
                    
                        connection.send(pickle.dumps({'what': 'db_cursor', 'cursor': result_set}))
                    else:
                        c.execute(s)
                        
                        connection.send(pickle.dumps({'what': 'db_ok'}))
                except sqlite3.Error, a:
                    connection.send(pickle.dumps({'what': 'db_error', 'message': a}))
                    
            connection.close()

        except KeyboardInterrupt:
            print 'Servidor encerrado\n'
            break
