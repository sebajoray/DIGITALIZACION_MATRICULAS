#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from flask import json
import json
from elasticsearch import Elasticsearch
from flask import Flask, render_template, make_response, jsonify, request

app = Flask(__name__)

PORT = 3200

es = Elasticsearch('http://localhost:9200', basic_auth=('seba', 'gemin8'), verify_certs=False)
cadena='cadena'
@app.route("/")
def home():
   return render_template("index.php")

@app.route("/matriculas", methods=["POST"])
def matricula():
  cadena = request.form.get("cadena") 
  result = es.search(
      index='matriculas2',
      query={'match': {'texto': cadena}}
  )
  all_hits =result['hits']['hits']
  data = []

  for num, doc in enumerate(all_hits):
    item=doc['_source']['path']
    print ("ruta::")
    item = item.replace("\\","/" )
    print(item)
    #item=doc['_source']['path']+'/'+doc['_source']['imagen']
    data.append(item)
    # print a few spaces between each doc for readability


  lista=[]  
  for item in data:
    if item not in lista:
        lista.append(item)

  return render_template("matriculas.html", result=lista, cadena=cadena)

@app.route("/verPdf")
def pdf():
  cadena = request.form.get("path") 
  return render_template("visor.html", path=path)

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host='0.0.0.0', port=PORT, debug=True)






