from langchain.prompts import PromptTemplate

summarize_text_prompt_template = """
请对我提供的文本进行阅读理解和摘要。你的回答应该包含一段对原文的简要概述，注意需使用列表的形式突出文本的关键信息和主要观点。请确保摘要既简洁明了又准确完整，以便让读者能够快速了解原文的核心内容。 
接下来。你需要处理的文本内容为：{text}
"""

SUMMARIZE_TEXT_PROMPT = PromptTemplate.from_template(summarize_text_prompt_template)

summarize_conversation_prompt_template = """
这是一段对话记录，其中涉及不同人物的交流。请仔细阅读以下对话，并根据其内容提供一个简洁、准确的摘要，以帮助快速理解对话的主要内容和要点。
对话记录如下：{conversation_text}
请根据上述对话内容，生成一个摘要，准确反映对话的主题和核心信息。
"""

SUMMARIZE_CONVERSATION_PROMPT = PromptTemplate.from_template(
    summarize_conversation_prompt_template
)
