from textcraft.utils.complex import init_config_develop
from textcraft.utils.convert_util import hit_to_json
from textcraft.vectors.es.ElasticsearchConnection import ElasticsearchConnection


class ESSearch:
    def bool_search(self, time, loginid):
        es = ElasticsearchConnection()
        body1 = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"metadata.time": {"lte": time}}},
                        {"match": {"metadata.loginid": loginid}},
                    ]
                }
            },
            "_source": ["text", "metadata"],  # 指定返回的数据字段
            "size": 5,  # 设置返回的结果数量
        }

        body2 = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"metadata.time": {"gte": time}}},
                        {"match": {"metadata.loginid": loginid}},
                    ]
                }
            },
            "_source": ["text", "metadata"],  # 指定返回的数据字段
            "size": 5,  # 设置返回的结果数量
        }

        hits1 = es.search(body1)
        hits2 = es.search(body2)
        combined_hits = sorted(
            hits1 + hits2, key=lambda doc: doc["_score"], reverse=True
        )
        return hit_to_json(combined_hits)


if __name__ == "__main__":
    init_config_develop(dialog_id="0")
    es_search = ESSearch()

    # print(es_search.bool_search("1699930207000", "2023111410514000002"))