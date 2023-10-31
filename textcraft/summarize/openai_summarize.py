from textcraft.summarize.summarize import Summarizer
from textcraft.models.llms.openai import openai


class OpenAISummarizer(Summarizer):
    def __init__(self):
        llm = openai
        super().__init__(llm)
