# TextCraft: amplify llm capabilities through langchain

## 🦖 介绍

 一种利用 [langchain](https://github.com/hwchase17/langchain) 思想实现的放大llm能力的应用，用以建立一套对中文场景与开源模型支持友好的llm应用解决方案。

## 🌟 Quickstart

1. 配置Python解释器

   Mac

   命令行下运行

   ```bash
   brew install python
   ```

   Windows

   在 python 官网 https://www.python.org/downloads/windows/ 上，选择最新的 Python 安装包，下载安装即可。

   安装完 Python，我们在命令行输入 python3，就可以启动 python 解释器，像下面这样

   ```text
   $ python3
   Python 3.9.6 (v3.9.6:db3ff76da1, Jun 28 2021, 11:49:53)
   [Clang 6.0 (clang-600.0.57)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   >>>
   ```

2. 配置环境变量

   复制.env.example修改文件名为.env，添加你的系统设置到.env文件

   复制config.json.example修改文件名为config.json，添加你的用户设置到config.json文件

3. 启动项目

   ```bash
   # Windows
   .\run.bat 
   # Mac/Linux
   .\run.sh
   ```

## 🐳 Docker 部署

- [配置Redis](https://garveys.notion.site/Docker-Compose-Redis-73141176df6440d8a9c4be0d0d5de3cf?pvs=4)
- [配置MongoDB](https://garveys.notion.site/Docker-Compose-MongoDB-b16680405b824adb8a30db92c131a4e4?pvs=4)

```bash
sudo docker-compose up -d
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