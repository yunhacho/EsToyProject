from flask import Flask
from flask import render_template
from flask import request
from elasticsearch import Elasticsearch
import json

from SearchAPI.PrefixSearch import PrefixSearch


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
	return render_template('searchHome.html')

@app.route('/search', methods=['GET'])
def search() :
    host = '0.0.0.0'; port = '9200'
    index = 'entire_krx_tckr'
    keyword = request.args.get('keyword')
    result = PrefixSearch(host, port, index).search(keyword)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
