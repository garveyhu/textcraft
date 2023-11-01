from textcraft.models.llms.llm_creator import LLMCreator
from textcraft.summarize.summarize import Summarizer


class OpenAISummarizer(Summarizer):
    def __init__(self):
        llm = LLMCreator.create_llm("openai")
        super().__init__(llm)
