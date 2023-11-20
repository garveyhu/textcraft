import streamlit as st

from textcraft.chains.conversation import Conversation
from textcraft.core.config import app_id, dialog_id, model_temperature
from textcraft.ui.streamlit_ui.utils import (
    transform_messages_to_streamlit_format,
    transform_to_custom_format,
)
from textcraft.utils.complex import init_config_develop
from textcraft.utils.redis_manager import RedisManager
from textcraft.vectors.es.es_store import ESStore

init_config_develop(dialog_id="0")
app = app_id()
dialog = dialog_id()


def handle_model_change():
    model = st.session_state.model_select0
    RedisManager().update_dialog_model(dialog, model)


def handle_temperature_change():
    temperature = st.session_state.temperature_slider0
    RedisManager().update_model_temperature(app, model, temperature)


with st.sidebar:
    model = st.selectbox(
        "LLM模型",
        ("qwen-turbo", "spark-v3", "ernie-bot-turbo", "gpt-3.5-turbo"),
        key="model_select0",
        on_change=handle_model_change,
    )
    temperature = st.slider(
        "温度",
        0.0,
        2.0,
        model_temperature(),
        0.1,
        key="temperature_slider0",  # 提供一个 key 用于在 session_state 中引用
        on_change=handle_temperature_change,
    )

st.title("💬 Chatbot")
st.caption("🚀 A general chatbot")
if "messages0" not in st.session_state:
    # 1.从ES中获取聊天记录
    msg_docs = ESStore().search_show()
    st.session_state["messages0"] = transform_messages_to_streamlit_format(msg_docs)

for msg in st.session_state.messages0:
    # 2.历史聊天记录初始化聊天框
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # 3.用户提问聊天框刷新
    st.session_state.messages0.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 4.调用LLM获得响应
    response = Conversation().chat_with_memory(prompt)

    # 5.将聊天记录存入ES
    ESStore().store_chat(transform_to_custom_format(prompt, response))

    # 6.AI响应聊天框刷新
    msg = {"role": "assistant", "content": response}
    st.session_state.messages0.append(msg)
    st.chat_message("assistant").write(response)
