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
  file = cont['filename']
  content = cont['content']
  if not file or not content:
    return "empty filename or content", 404
  if create_file(file, content):
    return "HTTP 201 CREATED", 201
  else:
    return "error while creating file", 400

@app.route(api_url+'/files/recently_created',methods=['POST'])
def create_recent_file():
  return "HTTP 404 NOT FOUND", 404

@app.route(api_url+'/files',methods=['DELETE'])
def delete_all_files():
  list = {}
  list["files"] = get_all_files()
  for idx, val in enumerate(list["files"]):
      if not remove_one_file(val):
        return "Error while deleting files", 400
  return "HTTP 200 OK", 200

@app.route(api_url+'/files/recently_created',methods=['DELETE'])
def delete_recent_files():
  return "HTTP 404 NOT FOUND", 404

@app.route(api_url+'/files',methods=['PUT'])
def put_file():
  return "HTTP 404 NOT FOUND", 404

@app.route(api_url+'/files/recently_created',methods=['PUT'])
def put_recent():
  return "HTTP 404 NOT FOUND", 404

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8081,debug='True')

