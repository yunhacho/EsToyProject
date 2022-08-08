# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import pprint

import elasticsearch
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import Search

class EsClient:
    def __init__(self,host,port):
        self.es = Elasticsearch(host=host, port=port)

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
            }
        }
        res = self.es.search(index=index, body=body)
        return res["hits"]["hits"]

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
        return res["hits"]["hits"]

def get_data(index):
    fname='myli001m0_20220803.csv'
    df = pd.read_csv(fname)
    '''
    if 'eng' in index:
    .
        df = df[df['myd_excg_no']! ='KRX']
    elif 'krx' in index:
        df = df[df['myd_excg_no']=='KRX']
    '''
    #[TODO] ETF 특정 필드 없는 row 처리
    df.dropna(inplace=True)
    source = df.to_dict(orient='records')
    return  source

def get_setting(fname, path=''):
    with open(path+fname, 'r', encoding='utf-8') as f:
        setting=json.load(f)
    return setting

class PrefixSearch:

    # auto-completion
    @staticmethod
    def auto_complete(es_suggest):
        info = [{'item': r['text'], 'oppr_tot_amt': r['_source']['oppr_tot_amt']} for r in es_suggest]
        info = sorted(info, key=lambda x: x['oppr_tot_amt'], reverse=True)[:10]
        return pd.DataFrame(info)

    # kor2eng
    @staticmethod
    def kor2eng():
        pass

    # eng2kor
    @staticmethod
    def eng2kor(es_eng2kor):
        info = [{'item': r['_source']['kor_item_name'], 'oppr_tot_amt': r['_source']['oppr_tot_amt']} for r in es_eng2kor]
        info = sorted(info, key=lambda x: x['oppr_tot_amt'], reverse=True)[:10]
        return pd.DataFrame(info)

    # typo-correct
    @staticmethod
    def typo_correct(es_typocorrect):
        info = [{'item': r['_source']['kor_item_name'], 'oppr_tot_amt': r['_source']['oppr_tot_amt']} for r in es_typocorrect]
        info = sorted(info, key=lambda x: x['oppr_tot_amt'], reverse=True)[:10]
        return pd.DataFrame(info)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    host='0.0.0.0'; port='9200'
    client = EsClient(host, port)

    index = 'entire_krx_tckr'
    fname = 'krx_setting.json'
    setting = get_setting(fname)

    #create index
    #client.delete_index(index)
    #client.create_index(index, setting)

    #insert data
    #bulk_data = get_data(index)
    #client.bulk_insert(index, bulk_data)

    # 자동완성
    res = client.suggest(index, "kor_item_completion", "삼")
    df=PrefixSearch.auto_complete(res)
    print(df)

    # eng2kor
    res = client.eng2kor(index, "tkatjdwjswk")
    df=PrefixSearch.eng2kor(res)
    print(df)

    # 오타교정
    res = client.eng2kor(index, "샴성전자")
    df=PrefixSearch.typo_correct(res)
    print(df)
