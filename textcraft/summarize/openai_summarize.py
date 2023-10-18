from langchain import OpenAI

from textcraft.summarize.summarize import Summarizer

class OpenAISummarizer(Summarizer):
    def __init__(self):
        llm = OpenAI(temperature=0.5)
        super().__init__(llm)