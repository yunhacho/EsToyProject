FROM docker.elastic.co/elasticsearch/elasticsearch:7.0.0
RUN yum install wget -y
RUN wget https://github.com/javacafe-project/elasticsearch-plugin/releases/download/v7.0.0/javacafe-analyzer-7.0.0.zip
RUN ["bin/elasticsearch-plugin", "install", "file:/usr/share/elasticsearch/javacafe-analyzer-7.0.0.zip"]
RUN ["bin/elasticsearch-plugin", "install", "analysis-nori"]
