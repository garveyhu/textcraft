import streamlit as st

from textcraft.core.inventory import inventory

st.title("Configurations")

selected_vector_store = st.selectbox("vector_store:", inventory.vector_store)
selected_llm = st.selectbox("llm:", inventory.llm)
selected_embedding = st.selectbox("embeddings:", inventory.embeddings)

if st.button("load"):
    st.write(f"已选择向量存储: {selected_vector_store}")
    st.write(f"已选择LLM模型: {selected_llm}")
    st.write(f"已选择嵌入模型: {selected_embedding}")
