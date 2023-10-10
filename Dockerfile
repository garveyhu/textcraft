# 使用官方Python镜像作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /usr/src/app

# 将依赖文件复制到容器中
COPY requirements.txt ./

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录内容复制到容器中
COPY . .

# 使用uvicorn运行应用
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
