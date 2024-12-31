# 📚 RAG Document Assistant

A powerful document question-answering system built with Streamlit and LangChain. This application allows users to upload PDF documents and ask questions about their content using state-of-the-art language models and embeddings.

![image](https://github.com/user-attachments/assets/6886f350-3592-4e16-8f4a-a022148818dd)


## 🌟 Features

- PDF document processing and analysis
- Advanced text chunking and embedding
- Semantic search capabilities
- Real-time question answering
- Interactive web interface
- Document context visualization

## 🛠️ Technologies Used

- **Framework**: Streamlit
- **LLM Provider**: Groq (Mixtral-8x7b-32768)
- **Embeddings**: Ollama (nomic-embed-text)
- **Vector Store**: FAISS
- **PDF Processing**: LangChain
- **Other Libraries**: 
  - langchain-groq
  - langchain-community
  - python-dotenv
  - PyPDF2

## 📋 Prerequisites

1. Python 3.8 or higher
2. Ollama installed on your system ([Install Ollama](https://ollama.ai/))
3. Groq API key ([Get API Key](https://console.groq.com/))

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/zeineb61romthana/rag-doc-assistant.git
cd rag-doc-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install streamlit langchain-community langchain-groq faiss-cpu python-dotenv ollama
```

4. Pull the embedding model:
```bash
ollama pull nomic-embed-text
```

## ⚙️ Configuration

1. Create a `.env` file in the project root:
```env
groq_api=your_groq_api_key_here
```

2. Make sure Ollama is running on your system:
```bash
ollama serve
```

## 💻 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and go to `http://localhost:8501`

3. Use the application:
   - Upload a PDF document
   - Click "Process Document" to embed the content
   - Enter your questions about the document
   - View responses and relevant document sections

## 🔍 How It Works

1. **Document Processing**:
   - PDF is uploaded and processed
   - Text is split into manageable chunks
   - Chunks are embedded using nomic-embed-text model

2. **Question Answering**:
   - User question is processed
   - Relevant document sections are retrieved using FAISS
   - Groq LLM generates response based on retrieved context

3. **Response Generation**:
   - Answer is displayed to user
   - Relevant document sections are shown
   - Processing time is displayed

## 🌟 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for the amazing framework
- [Groq](https://groq.com/) for the LLM API
- [Ollama](https://ollama.ai/) for the embedding model
- [Streamlit](https://streamlit.io/) for the web framework

