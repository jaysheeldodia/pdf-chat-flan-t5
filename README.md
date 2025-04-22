
# 📄 Chat with Your PDF using FLAN-T5 + LangChain + Gradio

This project allows you to **chat with the contents of any PDF** using a powerful combination of:

- 🔍 **LangChain** for document loading, chunking, retrieval
- 🤖 **FLAN-T5** (via Hugging Face) for natural language question answering
- 📁 **FAISS** for efficient vector search
- 🧠 **Sentence Transformers** for embedding chunks
- 🎨 **Gradio** for a sleek and simple interactive UI

---

## ✨ Features

- Upload any PDF and convert it to smart searchable chunks
- Ask natural questions about the PDF
- Uses generative QA (`google/flan-t5-large`)
- Works on CPU (no GPU required)
- Fully interactive web interface with Gradio

---

## 🚀 Demo

https://github.com/user-attachments/assets/933fd301-d6f0-46e1-ada3-ca91bd997223

---

## 🛠️ Installation

You can run this on your **local machine** or **Google Colab**.

### 🖥️ Local Setup

```bash
git clone https://github.com/jaysheeldodia/pdf-chat-flan-t5.git
cd pdf-chat-flan-t5

# Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### 🧪 In Google Colab

1. Copy the code from `app.py` into a Colab notebook cell.
2. Add `demo.launch(share=True)` at the end.
3. Run and get a public link instantly.

---

## 🧾 Dependencies

Install these with pip (or see `requirements.txt`):

```bash
gradio
langchain
transformers
pypdf
faiss-cpu
sentence-transformers
```

---

## 📦 How It Works

1. Upload a PDF → It gets chunked into 500-character segments.
2. Chunks are embedded using `sentence-transformers/all-MiniLM-L6-v2`.
3. Chunks are indexed with **FAISS**.
4. Your question is compared to all chunks using cosine similarity.
5. The top results are passed as context to `google/flan-t5-large` to generate an answer.

---

## 🖼️ Screenshot

Add a screenshot named `screenshot.png` in your repo to show the UI.

---

## 🧠 Model Notes

- LLM used: [`google/flan-t5-large`](https://huggingface.co/google/flan-t5-large)
- You can swap in other models (e.g., `mistralai/Mistral-7B-Instruct`) easily.

---

## 📌 TODO / Ideas

- [ ] Add support for multiple PDFs
- [ ] Enable chat history and multi-turn memory
- [ ] Add model selector in the UI
- [ ] Export Q&A session to text/markdown

---

## 📃 License

This project is open source under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [LangChain](https://github.com/hwchase17/langchain)
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [Gradio](https://github.com/gradio-app/gradio)
