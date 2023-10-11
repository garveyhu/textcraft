import configparser
config = configparser.ConfigParser()
config.read('config.ini')
# 读取配置参数
SPARK_APPID = config.get('myconfig', 'SPARK_APPID')
SPARK_API_KEY = config.get('myconfig', 'SPARK_API_KEY')
SPARK_API_SECRET = config.get('myconfig', 'SPARK_API_SECRET')
PINECONE_ENV = config.get('myconfig', 'PINECONE_ENV')
PINECONE_KEY = config.get('myconfig', 'PINECONE_KEY')