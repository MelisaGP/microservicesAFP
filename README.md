# microservicesAFP

#Acciones previas.

##Abrir puertos
En iptables:
Abro los siguientes puertos para utilizar la aplicación.
La aplicación actualmente está corriendo en el puerto 8081.

```python
-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 8080 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 8081 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 8082 -j ACCEPT
```

Reiniciar servicio de iptables
```python
service iptables restart
```

##Crear user file_system

```python
```

```python
useradd filesystem_user
passwd filesystem_user
```
Darle permisos de sudoer
```linux
usermod -G wheel filesystem_user
```

##Agregar usuario a sudoers
En visudo:


```python
root    ALL=(ALL)       ALL
operativos      ALL=(ALL)       ALL
python_user     ALL=(ALL)       ALL
filesystem_user ALL=(ALL)       ALL
```

![alt test]()

Archivo de funciones REST

```python

from flask import Flask, abort, request
import json

from ec import get_all_files, create_file, get_recent_files

app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/files',methods=['GET'])
def read_all_files():
  list = {}
  list["files"] = get_all_files()
  return json.dumps(list), 200

@app.route(api_url+'/files/recently_created',methods=['GET'])
def read_recent_file():
  list = {}
  list["files"] = get_recent_files()
  return json.dumps(list), 200

@app.route(api_url+'/files',methods=['POST'])
def read_create_file():
  cont = request.get_json(silent=True)
  file = cont['file']
  content = cont['content']
  if not file or not content:
    return "empty file or content", 404
  if create_file(file, content):
    return "CREATED", 200
  else:
    return "error while creating file", 400

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8081,debug='True')

```

##Archivo de comandos de apoyo de python

``` python
from subprocess import Popen, PIPE

def create_file(file, content):
  result1 = Popen(["echo","/home/systemfile_user/",content,">",file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  result1.wait()
  return True

def get_all_files():
  result1 = Popen(["ls","/home/filesystem_user","-p"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  result2 = Popen(["grep", "-v", "/"], stdin=result1.stdout, stdout=PIPE, stderr=PIPE)
  return result2.communicate()[0].split('\n')

def get_recent_files():
  result1 = Popen(["ls","/home/filesystem_user","-Art"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  result2 = Popen(["tail", "-n", "2"], stdin=result1.stdout, stdout=PIPE, stderr=PIPE)
  return result2.communicate()[0].split('\n')


```
