from typing import List
from http import HTTPStatus

import dashscope
from dashscope import TextEmbedding
from langchain.embeddings.base import Embeddings

from textcraft.config import Config

cfg = Config()
dashscope.api_key = cfg.qwen_api_key

class QwenEmbedding(Embeddings):

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        print("=======>embed_documents")
        return self.embed_with_str(texts, 0)

    def embed_query(self, text: str) -> List[float]:
        print("=======>embed_query")
        return self.embed_with_str(text, 1)

    def embed_with_str(self, text, type):
        print(type)
        resp = TextEmbedding.call(
            model=TextEmbedding.Models.text_embedding_v1,
            input=text)
        print(resp)
        if resp.status_code == HTTPStatus.OK:
            list = resp.output["embeddings"]
            if len(list) > 1:
                data = []
                for item in list:
                    data.append(item["embedding"])
                return data
            else:
                print(len(list[0]["embedding"]))
                if type == 0:
                    list2 = [list[0]["embedding"]]
                    return list2
                else:
                    return list[0]["embedding"]
        else:
            return resp