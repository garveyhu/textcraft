from textcraft.models.spark.spark_chat import Spark
from textcraft.summarize.summarize import Summarizer


class SparkSummarizer(Summarizer):
    def __init__(self):
        llm = Spark()
        super().__init__(llm)
