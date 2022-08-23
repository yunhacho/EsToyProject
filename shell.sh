#!/bin/bash

echo "Installing flask..."
pip install flask

echo "Installing Werkzeug..."
pip install -U Werkzeug

echo "Installing elasticsearch"
pip install elasticsearch

./Elasticsearch/execute.sh

cd Flask-Web
flask run
