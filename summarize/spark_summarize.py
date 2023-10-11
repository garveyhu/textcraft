from summarize.spark.SparkChat import Spark
from summarize.summarize import Summarizer

class SparkSummarizer(Summarizer):
    def __init__(self):
        llm = Spark()
        super().__init__(llm)