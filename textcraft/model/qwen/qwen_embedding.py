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
        return self.embed_with_str(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.embed_with_str(text)

    def embed_with_str(self, text):
        resp = TextEmbedding.call(
            model=TextEmbedding.Models.text_embedding_v1,
            input=text)
        # print(resp)
        if resp.status_code == HTTPStatus.OK:
            list = resp.output["embeddings"]
            if len(list) > 1:
                data = []
                for item in list:
                    data.append(item["embedding"])
                return data
            else:
                return list[0]["embedding"]
        else:
            return resp
