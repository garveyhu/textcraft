from elasticsearch import Elasticsearch

from textcraft.core.settings import settings

ES_SCHEME = settings.ES_SCHEME
ES_HOSTS = settings.ES_HOSTS
ES_PORT = settings.ES_PORT


class ElasticsearchConnection:
    def __init__(self):
        self.host = ES_HOSTS
        self.port = ES_PORT
        self.scheme = ES_SCHEME
        # 创建Elasticsearch连接对象
        self.connection = Elasticsearch(
            [{"scheme": self.scheme, "host": self.host, "port": self.port}]
        )

    def search(self, query):
        # 执行搜索查询，并返回结果
        response = self.connection.search(index="online_chat", body=query)
        return response["hits"]["hits"]

    def search_index(self, index_name, query):
        response = self.connection.search(index=index_name, body=query)
        return response["hits"]["hits"]
