from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

def summarize_file(file_obj):
    # 使用openai模型
    llm = OpenAI(temperature=0)

    # 定义文档拆分器
    text_splitter = CharacterTextSplitter(chunk_size = 3000, chunk_overlap = 200)

    # 从文件对象中读取长文本
    long_text = file_obj.read()

    # 使用文档拆分器切割长文本
    texts = text_splitter.split_text(long_text)

    docs = [Document(page_content=t) for t in texts[:3]]

    # 定义提示词模板
    prompt_template = """总结下文内容:
    {text}
    总结内容:"""
    
    # 创建提示词模板
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    # 通过map_prompt和combine_prompt参数设置使用的提示词模板，这里设置成一样的模板，当然你也可以设置成不一样的模板
    chain = load_summarize_chain(llm, chain_type="map_reduce", return_intermediate_steps=True, map_prompt=PROMPT, combine_prompt=PROMPT)

    result = chain({"input_documents": docs}, return_only_outputs=True)
    output_text = result.get('output_text', '')  # 使用get方法，如果'output_text'不存在，则返回空字符串
    return output_text.strip('\n')

# with open("AI\\LangChain\\file\\chat.txt", encoding='utf-8') as f:
#     result = summarize_file(f)
#     print(result)