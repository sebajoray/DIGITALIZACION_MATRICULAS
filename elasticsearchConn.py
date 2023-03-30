#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200', basic_auth=('seba', 'gemin8'), verify_certs=False)

es.index(
 index='matriculas',
 document={
  'nombre': 'Clorindo Pedro Gometti',
  'imagen': 'felizarg2.tiff'
 })

es.indices.refresh(index='matriculas')

print (es.info())