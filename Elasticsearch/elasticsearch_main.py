import json
import pprint
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers

class EsClient:
    def __init__(self,host,port):
        self.es = Elasticsearch(host=host, port=port, timeout=30, max_retries=10, retry_on_timeout=True)

    def create_index(self, index, body=None):
        if not self.es.indices.exists(index=index):
            res = self.es.indices.create(index=index, body=body)
            pprint.pprint(self.es.indices.get_mapping(index))
            return res

    def delete_index(self, index):
        if self.es.indices.exists(index=index):
            return self.es.indices.delete(index=index)

    def bulk_insert(self, index, sources):
        bulk_data = []
        for source in sources:
            id = source['topc_id']
            data = {"_index": index, "_id": id, "_source": source}
            bulk_data.append(data)
        return helpers.bulk(self.es, bulk_data)

    def search(self, index, body=None):
        if body is None:
            body = {
                "query":{
                    "match_all":{}
                }
            }

        #[TODO] 정확한 쿼리식인지 검증
        res = self.es.search(index=index, body=body)
        return res

    def analyze(self, index, analyzer, text):
        body={
            "analyzer": analyzer,
            "text": text
        }
        res=self.es.indices.analyze(index=index, body=body)
        return res['tokens']

    def get_term_vectors(self, index, id, fields):
        term_vectors = self.es.termvectors(index=index, id=id, fields=fields, offsets=False,
                            payloads=False, positions=False, field_statistics=False)['term_vectors']

        return term_vectors

    def suggest(self, index,field,prefix):
        body = {
          "suggest": {
            "s1": {
              "prefix": prefix,
              "completion": {
                "field": field,
                "size": 100
              }
            }
          }
        }
        res = self.es.search(index=index, body=body)
        return res['suggest']["s1"][0]["options"]

    def eng2kor(self, index, query):
        body={
            "query": {
                "match": {
                    "eng2kor_suggest": {
                        "query": query
                    }
                }
            },
            "size": 100
        }
        res = self.es.search(index=index, body=body)
        return res["hits"]["hits"]

    def kor2eng(self, index, query):
        body={
            "query": {
                "match": {
                    "kor2eng_suggest": {
                        "query": query
                    }
                }
            },
            "size": 100
        }
        res = self.es.search(index=index, body=body)
        return res["hits"]["hits"]

    def jamo(self, index, keyword):
        body={
          "query": {
            "match": {
              "kor_item_jamo": {
                "query": keyword
              }
            }
          },
           "size": 100,
           "sort": {
             "oppr_tot_amt": "desc"
           }
        }
        res = self.es.search(index=index, body=body)
        return res["hits"]["hits"]

    def chosung(self, index, keyword):
        body={
          "query": {
            "match": {
              "kor_item_chosung": {
                "query": keyword
              }
            }
          },
           "size": 100,
           "sort": {
             "oppr_tot_amt": "desc"
           }
        }
        res = self.es.search(index=index, body=body)
        return res["hits"]["hits"]

    #[TODO] 추후 수정 필요
    def typo_correct(self, index, text):
        body={
          "suggest":{
            "s1":{
              "text": text,
              "term":{
                "field": "spell_suggest"
              }
            }
          }
        }
        res = self.es.search(index=index, body=body)
        return res['suggest']["s1"][0]["options"]


if __name__ == '__main__':

    host='0.0.0.0'; port='9200'
    #index = 'entire_krx_tckr'
    index = [ 'general_topic', 'etf_topic']
    client = EsClient(host, port)

    #create index
    for idx in index:

        path = ''; fname = 'add_setting.json'
        with open(path+fname, 'r', encoding='utf-8') as f:
            setting = json.load(f)

        client.delete_index(idx)
        client.create_index(idx, setting)

        #insert data
        fname=f'myli001m0_{idx}_ver20220926.csv'
        df = pd.read_csv(fname)

        for col in ('item_keyword', 'item_category', 'item_brand', 'customer', 'supplier', 'competitor'):
            df[col] = df[col].apply(lambda x: eval(x))

        #[TODO] 추후 db 연결
        df.dropna(inplace=True)
        data = df.to_dict(orient='records')
        bulk_data = []
        for e in data:
            e['item_relation']={
                'customer': e['customer'],
                'supplier': e['supplier'],
                'competitor': e['competitor']
            }
            e.pop('customer', None)
            e.pop('supplier', None)
            e.pop('competitor', None)
            bulk_data.append(e)

        client.bulk_insert(idx, bulk_data)
