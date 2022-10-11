from flask import Flask
from flask import render_template
from flask import request
import json

from SearchAPI.PrefixSearch import PrefixSearch

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('searchHome.html')

@app.route('/search', methods=['GET'])
def search() :
    host = '0.0.0.0'; port = '9200'
    index = 'general_topic'
    keyword = request.args.get('keyword')
    result = PrefixSearch(host, port, index).search(keyword)
    return json.dumps(result)

@app.route('/brandsearch', methods=['GET'])
def brandSearch() :
    host = '0.0.0.0'; port = '9200'
    keyword = request.args.get('keyword')

    index = 'general_topic'
    result = PrefixSearch(host, port, index).brand(keyword)
    index = 'etf_topic'
    result += PrefixSearch(host, port, index).brand(keyword)

    return json.dumps(returnSort(result))

@app.route('/categorysearch', methods=['GET'])
def categorySearch() :
    host = '0.0.0.0';
    port = '9200'
    keyword = request.args.get('keyword')

    index = 'general_topic'
    result = PrefixSearch(host, port, index).category(keyword)
    index = 'etf_topic'
    result += PrefixSearch(host, port, index).category(keyword)

    return json.dumps(returnSort(result))

@app.route('/keywordsearch', methods=['GET'])
def keywordSearch() :
    host = '0.0.0.0';
    port = '9200'
    keyword = request.args.get('keyword')

    index = 'general_topic'
    result = PrefixSearch(host, port, index).keyword(keyword)
    index = 'etf_topic'
    result += PrefixSearch(host, port, index).keyword(keyword)

    return json.dumps(returnSort(result))

@app.route('/etfsearch', methods=['GET'])
def etfSearch() :
    host = '0.0.0.0'; port = '9200'
    index = 'etf_topic'

    keyword = request.args.get('keyword')
    result = PrefixSearch(host, port, index).search(keyword)
    return json.dumps(result)

def returnSort(self, source):
    result = list(set([tuple(t) for t in [(x['kor_item_name'], x['oppr_tot_amt']) for x in source]]))
    result = [{'item': x[0], 'oppr_tot_amt': x[1]} for x in result]
    return sorted(result, key=lambda x: (-x['oppr_tot_amt']))

if __name__ == '__main__':
    app.run()
