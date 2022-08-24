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
   return render_template("index.html")

@app.route("/matriculas", methods=["POST"])
def matricula():
  cadena = request.form.get("cadena") 
  result = es.search(
      index='matriculas',
      query={'match': {'texto': cadena}}
  )
  all_hits =result['hits']['hits']
  for num, doc in enumerate(all_hits):
    print (doc['_source']['path'])
   
    # print a few spaces between each doc for readability
    print ("\n\n")
  return render_template("matriculas.html", result=all_hits)

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host='0.0.0.0', port=PORT, debug=True)






