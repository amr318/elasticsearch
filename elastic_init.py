from elasticsearch import helpers, Elasticsearch
import requests
import csv
import os
import json


def initialize_elasticsearch():
    es = Elasticsearch()


    if es.indices.exists(index='my-index'):
        es.indices.delete(index='my-index', ignore=[400,404])

    with open('lyrics.csv') as f:
        reader = csv.DictReader(f)
        mapping = json.dumps({
            "lyrics": {
                "properties": {
                    "Artist": {
                        "index": "not_analyzed",
                        "type": "text"
                    },
                    "Song": {
                        "index": "not_analyzed",
                        "type": "text"
                    }
                }
            }
        })
        helpers.bulk(es, reader, index='my-index', doc_type='lyrics')
        #es.indices.put_mapping(index='my-index', doc_type='lyrics', body=mapping)


def format_csv(file):
    lines = [l for l in file]
    for line in lines:
        line[1] = line[1].replace(' ', '_')
        line[2] = line[2].replace(' ', '_')
    return lines


