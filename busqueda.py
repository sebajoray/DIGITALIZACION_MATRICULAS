#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from flask import json
import json
from elasticsearch import Elasticsearch
from flask import Flask, render_template, make_response, jsonify, request
import copy

app = Flask(__name__)

PORT = 3200

es = Elasticsearch('http://localhost:9200', basic_auth=('seba', 'gemin8'), verify_certs=False)
cadena='cadena'
@app.route("/")
def home():
   return render_template("index.php")

@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/matriculas", methods=["POST"])
def matricula():
  cadena = request.form.get("cadena") 
  lista={}
  print("++++++++++++++++++++++++++++++++", cadena)
  result = es.search(
      index='matriculas3',
      query={'match': {'rubroA': cadena}}
  )
  all_hits =result['hits']['hits']
  data = []
  for num, doc in enumerate(all_hits):
    item=doc['_source']['path']

    #item = item.replace("\\","/" )
    item=item.split("\\")[1]
    item=item.replace("-", "_").replace("(", "_").replace(")", "").replace(" ", "")
    #item=doc['_source']['path']+'/'+doc['_source']['imagen']
    data.append(item)
    # print a few spaces between each doc for readability
    print("-----------------rubroA:", item, doc['_score'])
    if item not in lista:
      lista[item] = ('rubroA', copy.deepcopy(doc['_score']))
      print('helloooooo', item, doc['_score'])
 

  result = es.search(
      index='matriculas3',
      query={'match': {'nroInscri': cadena}}
  )
  all_hits =result['hits']['hits']
  data = []

  for num, doc in enumerate(all_hits):
    item=doc['_source']['path']

    #item = item.replace("\\","/" )
    item=item.split("\\")[1]
    item=item.replace("-", "_").replace("(", "_").replace(")", "").replace(" ", "")
    #item=doc['_source']['path']+'/'+doc['_source']['imagen']
    data.append(item)
    # print a few spaces between each doc for readability
    if item not in lista:
        lista[item] = ('nroInscri', doc['_score'])
    else:
        if 'nroInscri' not in lista[item]:
          lista[item] = lista[item] + ('nroInscri', doc['_score']) 

  result = es.search(
      index='matriculas3',
      query={'match': {'anteDom': cadena}}
  )
  all_hits =result['hits']['hits']
  data = []

  for num, doc in enumerate(all_hits):
    item=doc['_source']['path']
    print ("ruta::")
    #item = item.replace("\\","/" )
    item=item.split("\\")[1]
    item=item.replace("-", "_").replace("(", "_").replace(")", "").replace(" ", "")
    #item=doc['_source']['path']+'/'+doc['_source']['imagen']
    data.append(item)
    # print a few spaces between each doc for readability

    if item not in lista:
        lista[item] = ('anteDom', doc['_score'])
    else:
        if 'anteDom' not in lista[item]:
          lista[item] = lista[item] + ('anteDom', doc['_score']) 

  result = es.search(
    index='matriculas3',
    query={'match': {'descrip': cadena}}
  )
  all_hits =result['hits']['hits']
  data = []

  for num, doc in enumerate(all_hits):
    item=doc['_source']['path']
    print ("-----------------descrip:", item, doc['_score'])
    #item = item.replace("\\","/" )
    item=item.split("\\")[1]
    item=item.replace("-", "_").replace("(", "_").replace(")", "").replace(" ", "")
    #item=doc['_source']['path']+'/'+doc['_source']['imagen']
    data.append(item)
    # print a few spaces between each doc for readability
    if item not in lista:
        lista[item] = ('descrip', doc['_score'])
    else:
        if 'descrip' not in lista[item]:
          lista[item] = lista[item] + ('descrip', doc['_score']) 

  return render_template("matriculas.html", result=lista, cadena=cadena)

@app.route("/visor", methods=["POST"])
def visor():
    archivo  = request.form.get("path") 
    print("cadena:" + archivo)
    return render_template("visor.html", path=archivo)

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host='0.0.0.0', port=PORT, debug=True)






