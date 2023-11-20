import anthropic
import streamlit as st
from textcraft.core.config import app_id, dialog_id, model_temperature

from textcraft.utils.complex import init_config_develop
from textcraft.utils.redis_manager import RedisManager

init_config_develop(dialog_id="2")
app = app_id()
dialog = dialog_id()


def handle_model_change():
    model = st.session_state.model_select1
    RedisManager().update_dialog_model(dialog, model)


def handle_temperature_change():
    temperature = st.session_state.temperature_slider1
    RedisManager().update_model_temperature(app, model, temperature)


with st.sidebar:
    model = st.selectbox(
        "LLM模型",
        ("qwen-turbo", "spark-v3", "ernie-bot-turbo", "gpt-3.5-turbo"),
        key="model_select1",
        on_change=handle_model_change,
    )
    temperature = st.slider(
        "温度",
        0.0,
        2.0,
        model_temperature(),
        0.1,
        key="temperature_slider1",  # 提供一个 key 用于在 session_state 中引用
        on_change=handle_temperature_change,
    )

st.title("📝 File Q&A")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    article = uploaded_file.read().decode()
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key="")
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-v1",  # "claude-2" for Claude 2 model
        max_tokens_to_sample=100,
    )
    st.write("### Answer")
    st.write(response.completion)
