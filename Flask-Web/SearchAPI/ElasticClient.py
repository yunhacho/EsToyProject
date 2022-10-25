import json
import pprint
from elasticsearch import Elasticsearch
from elasticsearch import helpers

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

    def get_setting(self, fname, path=''):
        with open(path + fname, 'r', encoding='utf-8') as f:
            setting = json.load(f)
        return setting

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
        return [ t['token'] for t in res['tokens'] ]

    def get_term_vectors(self, index, id, fields):
        term_vectors = self.es.termvectors(index=index, id=id, fields=fields, offsets=False,
                            payloads=False, positions=False, field_statistics=False)['term_vectors']

        return term_vectors

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
              "kor_item_name": {
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

    def multi_engkor_eng(self, index, keyword):
        body={
          "query":{
            "multi_match": {
              "query": keyword,
              "fields": ["kor2eng_suggest", "eng2kor_suggest", "item_eng_dtl_name"]
            }
          },
          "size": 100,
           "sort": {
             "oppr_tot_amt": "desc"
           }
        }
        res = self.es.search(index=index, body=body)
        return res["hits"]["hits"]

    def keyword(self, index, keyword):
        body={
          "query": {
            "term": {
              "item_keyword": keyword
            }
          },
          "size": 100,
          "sort": {
            "oppr_tot_amt": "desc"
          }
        }
        res = self.es.search(index=index, body=body)
        return res["hits"]["hits"]

    def brand(self, index, keyword):
        body={
          "query": {
            "bool": {
              "must": [
                {
                  "nested": {
                    "path": "item_brand",
                    "query": {
                      "bool": {
                        "must": [
                          {
                            "term": {
                              "item_brand.brand": {
                                "value": keyword
                              }
                            }
                          }
                        ]
                      }
                    }
                  }
                }
              ]
            }
          },
          "size": 100,
          "sort": {
            "oppr_tot_amt": "desc"
          }
        }
        res = self.es.search(index=index, body=body)
        return res["hits"]["hits"]


    def category(self, index, keyword):
        body={
          "query": {
            "bool": {
              "must": [
                {
                  "nested": {
                    "path": "item_category",
                    "query": {
                      "bool": {
                        "must": [
                          {
                            "term": {
                              "item_category.category": {
                                "value": keyword
                              }
                            }
                          }
                        ]
                      }
                    }
                  }
                }
              ]
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


if __name__ == "__main__":
    host='0.0.0.0'; port='9200'
    index = 'entire_krx_tckr'
    client = EsClient(host, port)

    text = "삼성전"
    analyzer="eng_topic_index_analyzer"
    res = client.analyze(index, analyzer, text)
    print(res)

    text="삼성전"
    analyzer = "eng2kor_analyzer"
    res = client.analyze(index, analyzer, text)
    print(res)

    text="삼성전"
    analyzer = "kor2eng_analyzer"
    res = client.analyze(index, analyzer, text)
    print(res)
