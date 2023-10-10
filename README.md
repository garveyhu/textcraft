# LangChain-连接LLM

## [Introduction](https://python.langchain.com/docs/get_started/introduction)

**LangChain** is a framework for developing applications powered by language models. It enables applications that:

- **Are context-aware**: connect a language model to sources of context (prompt instructions, few shot examples, content to ground its response in, etc.)
- **Reason**: rely on a language model to reason (about how to answer based on provided context, what actions to take, etc.)

The main value props of LangChain are:

1. **Components**: abstractions for working with language models, along with a collection of implementations for each abstraction. Components are modular and easy-to-use, whether you are using the rest of the LangChain framework or not
2. **Off-the-shelf chains**: a structured assembly of components for accomplishing specific higher-level tasks

Off-the-shelf chains make it easy to get started. For complex applications, components make it easy to customize existing chains and build new ones.

## Summarize

使用LangChain对文档进行摘要总结

#### 运行项目

确保安装python解释器

```bash
pip install -r requirements.txt
nohup ./start.sh &
```

也可以通过docker构建，打开终端，进入包含`Dockerfile`的项目目录，然后运行以下命令：

```bash
docker build -t langchain:v1 .
docker run -d --name langchain_1 -p 8000:8000 --env-file .env langchain:v1
```

#### 使用LangChain集成的LLM接口

**使用 Web 浏览器进行测试**

FastAPI 自动生成了一个交互式API文档，你可以在浏览器中访问它。

1. 在浏览器地址栏输入：`http://localhost:8000/docs`
2. 这会打开一个交互式界面，你可以点击“Try it out”按钮，然后上传一个文件进行测试。

任何一种方法都会返回一个包含摘要的JSON对象。

注意：确保FastAPI应用正在运行，否则上面的请求将无法工作。如果你更改了host或端口，请相应地更新URL。

![image-20231009165651583](http://124.220.51.225/images/web/images/large/fastapi.jpg)