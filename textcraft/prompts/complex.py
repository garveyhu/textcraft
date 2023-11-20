from langchain.prompts import PromptTemplate

_HISTORY_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context.

Relevant pieces of previous conversation:
{history}

(You do not need to use these pieces of information if not relevant)

Current conversation:
Human: {input}
AI:"""
HISTORY_PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=_HISTORY_TEMPLATE
)
