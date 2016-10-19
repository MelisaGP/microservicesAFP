# PRIMER EXAMEN PARCIAL - ANDRES PINEROS

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

##Crear el ambiente en /home/filesystem_user

```python
mkdir envs
mkdir flaskExam

cd envs
virtualenv flask_env
. flask_env/bin/activate

pip install Flask
pip freeze > requirements.txt
pip install -r requirements.txt
```
#Implementación de la solución

##Crear scripts para servicios REST
e.py contendrá todos los servicios rest
ec.py contendrá todos los métodos de apoyo de python.
e.py importa los métodos de ec.py para responder a las solicitudes REST.

```python
cd ..
cd flaskExam
touch e.py
touch ec.py
```

###Archivo de funciones REST:
files GET -> Obtiene todos los archivos de la carpeta home de filesystem_user. Excluye archivos ocultos y carpetas.

files POST -> Agrega un nuevo archivo. Obtiene los parámetros de un objeto JSON (filename, content).

files DELETE -> Elimina todos los archivos de la carpeta. Aprovecha files GET para esto. No elimina los archivos ocultos ni las
carpetas.

files PUT -> 404

files/recently_created GET -> Obtiene los dos archivos más recientemente modificados o creados.

files/recently_created POST -> 404

files/recently_created PUT -> 404

files/recently_created DELETE  -> 404

```python
from flask import Flask, abort, request
import json

from ec import get_all_files, create_file, get_recent_files, remove_one_file

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

@app.route(api_url+'/files',methods=['DELETE'])
def delete_all_files():
  list = {}
  list["files"] = get_all_files()
  for idx, val in enumerate(list["files"]):
    if not remove_one_file(val)
      return "Error while deleting files", 400
  return "DELETED ALL HOME FILES", 200

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8081,debug='True')

```

###Archivo de comandos de apoyo de python

create_file -> Sirve para crear una archivo con un contenido específico.
Params: file: nombre del archivo.    content: contenido (texto) del archivo.

get_all_files -> Sirve para visualizar todos los archivos. Excluye archivos ocultos y carpetas.

get_recent_files -> Muestra los últimos 2 archivos creados o modificados.

remove_all_files -> Elimina todos los archivos del home de filesystem_user. No elimina carpetas ni archivos ocultos.

``` python

from subprocess import Popen, PIPE

def create_file(file, content):
  result1 = Popen(["touch",'/home/filesystem_user/'+file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  log = open('/home/filesystem_user/'+file, 'w')
  log.write(content)
  log.flush()
  return True

def get_all_files():
  result1 = Popen(["ls","/home/filesystem_user","-p"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  result2 = Popen(["grep", "-v", "/"], stdin=result1.stdout, stdout=PIPE, stderr=PIPE)
  return result2.communicate()[0].split('\n')

def get_recent_files():
  result1 = Popen(["ls","/home/filesystem_user","-Art"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  result2 = Popen(["tail", "-n", "2"], stdin=result1.stdout, stdout=PIPE, stderr=PIPE)
  return result2.communicate()[0].split('\n')

def remove_one_file(file):
  process = Popen(["rm", "/home/filesystem_user/"+file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  process.wait()
  return True

```

## Pruebas en POSTMAN
A continuación se verificará con un flujo de acciones el funcionamiento de los servicios REST.

### Verifico con el files GET que no hayan archivos.


### Agrego 3 archivos con el file POST


### Verifico el nombre y el contenido desde la consola.


### Verifico la existencia con files GET


### Verifico los ultimos últimos 2 archivos/carpetas modificados con file/recently_created GET


### Elimino los archivos con files DELETE


### Verifico que se hayan eliminado con files GET


