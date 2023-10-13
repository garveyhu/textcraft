FROM python:3.10

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -e .

# 使用uvicorn运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
