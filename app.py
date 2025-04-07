# Install dependencies first (Colab-friendly)
# !pip install gradio langchain transformers pypdf faiss-cpu sentence-transformers

import gradio as gr
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import tempfile
import os

# Global variables to store retriever and chain
retriever = None
qa_chain = None

def load_pdf_and_build_chain(pdf_path):
    global retriever, qa_chain

    try:
        # Read PDF from path passed by Gradio
        with open(pdf_path, "rb") as f_in, tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(f_in.read())
            tmp.flush()
            actual_pdf_path = tmp.name

        # Load and split PDF
        loader = PyPDFLoader(actual_pdf_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)

        # Create FAISS index
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.from_documents(docs, embeddings)
        retriever = db.as_retriever()

        # Load FLAN-T5 model
        model_name = "declare-lab/flan-alpaca-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)
        llm = HuggingFacePipeline(pipeline=pipe)

        # Build Retrieval QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )

        return "✅ PDF processed and chain built. Ask away!"

    except Exception as e:
        import traceback
        return f"❌ Error: {str(e)}\n\n{traceback.format_exc()}"

def ask_question_gradio(query):
    if not qa_chain:
        return "⚠️ Please upload and process a PDF first."

    try:
        result = qa_chain.run(query)
        return result
    except Exception as e:
        return f"❌ Error during answering: {str(e)}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📄 Chat with your PDF using FLAN-T5 + LangChain")

    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        upload_btn = gr.Button("Process PDF")

    status_output = gr.Textbox(label="Status", interactive=False)

    upload_btn.click(fn=load_pdf_and_build_chain, inputs=pdf_input, outputs=status_output)

    question_input = gr.Textbox(label="Ask a Question")
    answer_output = gr.Textbox(label="Answer", lines=5)

    question_input.submit(fn=ask_question_gradio, inputs=question_input, outputs=answer_output)

demo.launch()
