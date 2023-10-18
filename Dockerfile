FROM python:3.10

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -e .

CMD ["./start.sh"]
