import gradio as gr

from textcraft.vectors.pinecone_qa import vector_qa
from textcraft.function.summarize.summarizer import Summarizer


def summarizer_router(file, long_text, question):
    if file:
        decoded_content = file.read().decode("utf-8")
        summary = Summarizer().summarize_text(decoded_content)
    elif long_text:
        summary = Summarizer().summarize_text(long_text)
    elif question:
        summary = vector_qa(question)
    return summary


iface = gr.Interface(
    fn=summarizer_router,
    inputs=[
        gr.File(label="Upload a Text File"),
        gr.Textbox("text", label="Enter Text"),
        gr.File(label="Upload a Text File for Spark Summarizer"),
        gr.Textbox("text", label="Enter Text for Spark Summarizer"),
        gr.Textbox("text", label="Ask a Question"),
    ],
    outputs="text",
    title="Text Summarization and Q&A",
    description="Upload a text file or enter text for summarization, or ask a question for Q&A.",
)

if __name__ == "__main__":
    iface.launch()
