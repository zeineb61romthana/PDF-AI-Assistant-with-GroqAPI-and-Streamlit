# 📄 PDF-AI Assistant with GroqAPI and Streamlit

This project is an **AI-powered assistant** that utilizes **GroqAPI** for generating intelligent chat responses based on user inputs. Additionally, it allows users to upload PDFs, extracts relevant text, and uses the extracted content to enhance the responses. The application is built using **Streamlit** for a seamless user interface.

## ✨ Key Features:

- **Interactive Chat with AI**: Users can engage in real-time conversations with AI models, powered by **Groq**'s large language models (e.g., `llama3`, `gemma`).
- **PDF Upload & Text Extraction**: Users can upload PDF files, from which the app extracts text using **PyPDF2**. Relevant sections of the PDF are included in the AI's responses.
- **Model Selection**: The app allows users to choose from a selection of available models like `llama3-70b`, `gemma-7b-it`, etc., ensuring customizable interactions.
- **Streamed Responses**: The app streams responses in real time for a smooth user experience, even for large language models.
- **Search PDF Content**: Users can search for specific content from within the uploaded PDF to provide context for the AI responses.

## 🛠️ Technologies and Libraries:

- **Python**: Core programming language.
- **Streamlit**: Provides the interactive user interface.
- **Groq API**: Handles communication with large language models to generate chat responses.
- **PyPDF2**: Extracts text from PDF documents.
- **dotenv**: Manages environment variables securely.
- **Pathlib**: For handling filesystem paths in an object-oriented manner.

## 🚀 How It Works:

1. **Upload a PDF**: Upload a PDF document containing relevant content (e.g., workout plans, research papers).
2. **Ask Questions**: Type a query in the chat, and the AI will provide a response.
3. **AI with Context**: If a PDF is uploaded, the app searches for relevant text in the document and incorporates that information into the AI's response.
4. **Real-Time Streaming**: Watch as responses are generated and streamed to the user interface.

## 🛠️ Installation and Setup:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
