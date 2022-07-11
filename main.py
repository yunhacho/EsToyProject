# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import pprint

import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import client
from elasticsearch import helpers

class EsClient:
    def __init__(self,host,port):
        self.es = Elasticsearch(f'{host}{port}')

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

def get_data(index):
    fname='myli010m0_es.csv'
    df = pd.read_csv(fname)
    if 'eng' in index:
        df = df[df['myd_excg_no']!='KRX']
    elif 'krx' in index:
        df = df[df['myd_excg_no']=='KRX']

    #[TODO] ETF 특정 필드 없는 row 처리
    df.dropna(inplace=True)
    source = df.to_dict(orient='records')
    return  source

def get_setting(fname, path=''):
    with open(path+fname, 'r', encoding='utf-8') as f:
        setting=json.load(f)
    return setting

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    host='https://localhost:'; port='9200'
    client = EsClient(host, port)

    index = 'entire_krx_tckr'
    fname = 'krx_setting.json'
    setting = get_setting(fname)


    #create index
    client.delete_index(index)
    client.create_index(index, setting)

    #insert data
    bulk_data = get_data(index)
    client.bulk_insert(index, bulk_data)


    id = "CP0000000008"  # 삼성전자 id #"CP0000001663" 스튜디오 드래곤
    field = "bzns_otln_dtl_text" #"kor_item_name" #"bzns_otln_dtl_text" # 종목상세
    term_vectors = client.get_term_vectors(index, id, field)

    print(term_vectors[field]['terms'])
    terms=[]
    term_freq=[]
    for term, freq in term_vectors[field]['terms'].items():
        terms.append(term)
        term_freq.append(freq['term_freq'])


    df=pd.DataFrame({'term': terms, 'term_frequency':term_freq})
    print(df)

    query = '''
        {
          "query": {
            "multi_match": {
              "query": "tkatjdwjswk",
              "fields": ["ftst_tckrno","bzns_otln_dtl_text", "kor_item_name^3",
              "chosung",
              "jamo",
              "engtokor"]
            }
          },
            "sort":{
            "oppr_tot_amt": {
              "order": "desc"
            }
          }
        }
    '''
    '''
    res = client.search(index, query)
    for r in res['hits']['hits']:
        print(json.dumps(r['_source'], indent=2, ensure_ascii=False))
    '''