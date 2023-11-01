from textcraft.summarize.summarize import Summarizer
from textcraft.models.llms.openai import get_openai


class OpenAISummarizer(Summarizer):
    def __init__(self):
        llm = get_openai()
        super().__init__(llm)
