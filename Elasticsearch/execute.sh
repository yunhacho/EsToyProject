#!/bin/bash

if docker ps | grep es
then 
	echo "Elasticsearch is already running"
else
	echo "docker compose up"
	docker compose -f Docker/ElasticsearchKibana.yaml up -d

	if docker ps | grep es 
	then 
		echo "Elasticsearch is running"
	else	
		echo "[Error] Failed to execute Elasticsearch"
	fi
fi 
