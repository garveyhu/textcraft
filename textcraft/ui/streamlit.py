import streamlit as st

from textcraft.ui.inventory import inventory

st.title("Configurations")

selected_llm = st.selectbox("llm:", inventory.llm)
selected_embedding = st.selectbox("embeddings:", inventory.embeddings)

if st.button("load"):
    st.write(f"已选择LLM模型: {selected_llm}")
    st.write(f"已选择嵌入模型: {selected_embedding}")
