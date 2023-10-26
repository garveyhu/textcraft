# TextCraft: amplify llm capabilities through langchain

## 🦖 介绍

 一种利用 [langchain](https://github.com/hwchase17/langchain) 思想实现的放大llm能力的应用，用以建立一套对中文场景与开源模型支持友好的llm应用解决方案。

## 🌟 Quickstart

1. 配置环境变量

   复制.env.template修改拓展名为.env，添加你的api keys到.env文件

2. 启动项目

   ```bash
   # windows
   .\run.bat 
   # linux
   .\run.sh
   ```

## 🐳 Docker 部署

进入包含`Dockerfile`的项目目录，然后运行以下命令：

```bash
sudo docker build -t textcraft:v1 .
# 和宿主机共享网络，设置代理变量
sudo docker run --network host -d -e https_proxy=http://127.0.0.1:7890 -e http_proxy=http://127.0.0.1:7890 -e all_proxy=socks5://127.0.0.1:7890 --name textcraft_1 -p 8000:8000 textcraft:v1
```

## 🚁 模型支持

#### LLM 模型支持

在线 LLM 模型目前已支持：

- [ChatGPT](https://api.openai.com/)
- [讯飞星火](https://xinghuo.xfyun.cn/)
- [百度文心一言](https://yiyan.baidu.com/)
- [阿里云通义千问](https://dashscope.aliyun.com/)
- [百川](https://www.baichuan-ai.com/home#api-enter) (个人用户 API_KEY 暂未开放)

#### Embedding 模型支持

- [OpenAI/text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings)
- [阿里云通义千问](https://dashscope.aliyun.com/)

## 🦴 功能示例

#### API

通过FastAPI 自动生成了一个交互式API文档，打开浏览器访问：

1. 浏览器地址栏输入：`http://127.0.0.1:8000/docs`
2. 在FastAPI界面，选择API点击“Try it out”，然后对API进行测试。

![image-20231009165651583](http://124.220.51.225/images/archer/fastapi.jpg)

#### WebUI

通过Gradio可视化LLM能力，打开浏览器访问：

1. 浏览器地址栏输入：`http://127.0.0.1:7860/`
2. 在Gradio界面，通过对话框对LLm进行测试。

![image-20231009165651583](http://124.220.51.225/images/archer/gradio.jpg)