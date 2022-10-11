# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import pandas as pd
from . import ElasticClient

class KeywordSearch:
    def __init__(self, host, port, index):
        self.es = ElasticClient.EsClient(host, port)
        self.index = index

    def keyword(self, keyword):
        es_keyword = self.es.keyword(self.index, keyword)
        source = self._get_data(es_keyword)
        return self._search(source)

    def brand(self, keyword):
        es_brand = self.es.brand(self.index, keyword)
        source = self._get_data(es_brand)
        return self._search(source)

    def category(self, keyword):
        es_category = self.es.category(self.index, keyword)
        source = self._get_data(es_category)
        return self._search(source)

    def _get_data(self, es_result):
        return [ element["_source"] for element in es_result]

    def _search(self, source):
        result = list(set([tuple(t) for t in [(x['kor_item_name'], x['oppr_tot_amt']) for x in source]]))
        result = [{'item': x[0], 'oppr_tot_amt': x[1]} for x in result]
        return sorted(result, key=lambda x: (-x['oppr_tot_amt']))


if __name__ == "__main__":

    host = '0.0.0.0'; port = '9200'
    index = 'general_topic'
    api = KeywordSearch(host, port, index)

    keyword = '삼성전자'
    search_result = api.keyword(keyword)
    print(json.dumps(search_result, indent=2))