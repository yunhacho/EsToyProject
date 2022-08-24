# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import pandas as pd
from . import ElasticClient

class PrefixSearch:
    # auto-completion
    def __init__(self, host, port, index):
        self.es = ElasticClient.EsClient(host, port)
        self.index = index

    def kor2eng(self, keyword):
        es_kor2eng = self.es.kor2eng(self.index, keyword)
        return self._get_data(es_kor2eng)

    def eng2kor(self, keyword):
        es_eng2kor = self.es.eng2kor(self.index, keyword)
        return self._get_data(es_eng2kor)

    def jamo(self, keyword):
        es_jamo = self.es.jamo(self.index, keyword)
        return self._get_data(es_jamo)

    def chosung(self, keyword):
        es_chosung = self.es.chosung(self.index, keyword)
        return self._get_data(es_chosung)

    def multi_engkor_eng(self, keyword):
        es_multi = self.es.multi_engkor_eng(self.index, keyword)
        return self._get_data(es_multi)

    #[TODO] 추후수정
    def typo_correct(self, keyword):
        es_typocorrect = self.es.typo_correct(self.index, keyword)
        info = [{'item': r['text'], 'score':r['score']} for r in es_typocorrect]
        info = sorted(info, key=lambda x: -x['score'])
        return info

    def _get_data(self, es_result):
        return [ element["_source"] for element in es_result]

    def search(self, keyword):
        multi_engkor_eng = self.multi_engkor_eng(keyword)
        jamo = self.jamo(keyword)
        chosung = self.chosung(keyword) if not jamo else []

        result = multi_engkor_eng + jamo + chosung
        result = list(set([tuple(t) for t in [(x['kor_item_name'], x['oppr_tot_amt']) for x in result]]))
        result = [{'item': x[0], 'oppr_tot_amt': x[1]} for x in result]
        return sorted(result, key=lambda x: (-x['oppr_tot_amt']))


if __name__ == "__main__":

    host = '0.0.0.0'; port = '9200'
    index = 'entire_krx_tckr'
    api = PrefixSearch(host, port, index)

    keyword = '삼성전자'
    search_result = api.search(keyword)
    print(json.dumps(search_result, indent=2))