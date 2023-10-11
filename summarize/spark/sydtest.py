
import json
from urllib.parse import urlparse
import requests


class SydllmReq(object):

    def __init__(self,  url):
        self.host = urlparse(url).netloc
        self.path = urlparse(url).path
        self.url = url

    def get_Result(self, text):
        param_dict = {
            'prompt':  text
        }
        response = requests.post(url=self.url, json=param_dict)
        print(response)
        result = ""
        if response.status_code == 200:
            result = json.loads(response.content.decode('utf-8'))
        print(result)


if __name__ == "__main__":
    # 测试时候在此处正确填写相关信息即可运行
    emb = SydllmReq(url="http://172.16.0.112:8000/")
    emb.get_Result('13除以3等于几？精确到小数点后两位')
