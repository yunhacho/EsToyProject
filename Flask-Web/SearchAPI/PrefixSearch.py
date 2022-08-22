# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import pandas as pd
from SearchAPI.EsClient import EsClient

def get_data(index):
    fname='myli001m0_20220810.csv'
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



class PrefixSearch:
    # auto-completion
    def __init__(self, host, port, index):
        self.es = EsClient(host, port)
        self.index = index

    def auto_complete(self, field, keyword):
        es_suggest = self.es.suggest(self.index, field, keyword)
        info = [{'item': r['text'], 'oppr_tot_amt': r['_source']['oppr_tot_amt']} for r in es_suggest]
        info = sorted(info, key=lambda x: (-x['oppr_tot_amt']))
        return info

    def kor2eng(self, keyword):
        es_kor2eng = self.es.kor2eng(self.index, keyword)
        info = [{'item': r['_source']['kor_item_name'], 'oppr_tot_amt': r['_source']['oppr_tot_amt']} for r in es_kor2eng]
        info = sorted(info, key=lambda x: (-x['oppr_tot_amt']))
        return info

    def eng2kor(self, keyword):
        es_eng2kor = self.es.eng2kor(self.index, keyword)
        info = [{'item': r['_source']['kor_item_name'], 'oppr_tot_amt': r['_source']['oppr_tot_amt'] } for r in es_eng2kor]
        info = sorted(info, key=lambda x: (-x['oppr_tot_amt']))
        return info

    def jamo(self, keyword):
        es_jamo = self.es.jamo(self.index, keyword)
        info = [{'item': r['_source']['kor_item_name'], 'oppr_tot_amt': r['_source']['oppr_tot_amt']} for r in es_jamo]
        return info

    def chosung(self, keyword):
        es_chosung = self.es.chosung(self.index, keyword)
        info = [{'item': r['_source']['kor_item_name'], 'oppr_tot_amt': r['_source']['oppr_tot_amt']} for r in es_chosung]
        return info

    #[TODO] 추후수정
    def typo_correct(self, keyword):
        es_typocorrect = self.es.typo_correct(self.index, keyword)
        info = [{'item': r['text'], 'score':r['score']} for r in es_typocorrect]
        info = sorted(info, key=lambda x: -x['score'])
        return info

    def search(self, keyword):
        '''
        [TODO]
        - 신라젠 입력 시, 초성 메서드가 ㅅㄹㅈ 에 해당하는 다른 종목명도 들고옴
        1) 웹서버에서 초성 확인 -> 초성 메서드 호출
        - 신라 입력 시, ㅅㄹ 에 해당하는 종목명이 시총 순으로 정렬됨 -> 신라~가 하단에 위치
        '''

        kor2eng = self.kor2eng(keyword)
        eng2kor = self.eng2kor(keyword)
        jamo = self.jamo(keyword)
        chosung = self.chosung(keyword) if not jamo else []

        result = kor2eng + eng2kor + jamo + chosung
        result = list(set([tuple(t) for t in [(x['item'], x['oppr_tot_amt']) for x in result]]))
        result = [{'item': x[0], 'oppr_tot_amt': x[1]} for x in result]
        return sorted(result, key=lambda x: (-x['oppr_tot_amt']))


if __name__ == "__main__":

    host = '0.0.0.0'; port = '9200'
    index = 'entire_krx_tckr'
    api = PrefixSearch(host, port, index)

    keyword = '삼성전자'
    search_result = api.search(keyword)