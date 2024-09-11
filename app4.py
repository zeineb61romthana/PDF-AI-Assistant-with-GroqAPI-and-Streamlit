import os  # To interact with the operating system and environment variables.
import streamlit as st  # To create and run interactive web applications directly through Python scripts.
from pathlib import Path  # To provide object-oriented filesystem paths.
from dotenv import load_dotenv  # To load environment variables from a .env file.
from groq import Groq  # To interact with Groq's API for executing ML models.
import PyPDF2  # To extract text from PDF documents.

# Load environment variables from .env at the project root
project_root = Path(__file__).resolve().parent
load_dotenv(project_root / ".env")

class GroqAPI:
    """Handles API operations with Groq to generate chat responses."""
    def __init__(self, model_name: str):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = model_name

    # Internal method to fetch responses from the Groq API
    def _response(self, message):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0,
            max_tokens=4096,
            stream=True,
            stop=None,
        )

    # Generator to stream responses from the API
    def response_stream(self, message):        
        for chunk in self._response(message):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class Message:
    """Manages chat messages within the Streamlit UI."""
    system_prompt = "You are a professional AI. Please generate responses in English to all user inputs."

    # Initialize chat history if it doesn't exist in session state
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": self.system_prompt}]

    # Add a new message to the session state
    def add(self, role: str, content: str):
        st.session_state.messages.append({"role": role, "content": content})

    # Display all past messages in the UI, skipping system messages
    def display_chat_history(self):
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Stream API responses to the Streamlit chat message UI
    def display_stream(self, generater):
        with st.chat_message("assistant"):
            return st.write_stream(generater)

class ModelSelector:
    """Allows the user to select a model from a predefined list."""
    def __init__(self):
        # List of available models to choose from
        self.models = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]

    # Display model selection in a sidebar with a title
    def select(self):
        with st.sidebar:
            st.sidebar.title("Groq Chat with Llama3 + α")
            return st.selectbox("Select a model:", self.models)

def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

def search_pdf_for_relevant_text(pdf_text, query):
    """Search PDF text for paragraphs relevant to the user query."""
    query_lower = query.lower()
    relevant_paragraphs = [para for para in pdf_text.split('\n\n') if query_lower in para.lower()]
    return "\n\n".join(relevant_paragraphs[:5])  # Limit to 5 paragraphs to avoid exceeding token limits

# Entry point for the Streamlit app
def main():
    # Sidebar for uploading the PDF document
    st.sidebar.title("Upload PDF Document")
    pdf_file = st.sidebar.file_uploader("Upload a PDF document", type="pdf")

    pdf_text = ""
    if pdf_file:
        # Extract text from the uploaded PDF
        pdf_text = extract_text_from_pdf(pdf_file)
        st.sidebar.write("PDF text successfully extracted!")

    user_input = st.chat_input("Enter message to AI models...")
    model = ModelSelector()
    selected_model = model.select()

    message = Message()

    if user_input:
        # Search for relevant content in the PDF
        relevant_pdf_text = search_pdf_for_relevant_text(pdf_text, user_input)

        # Combine user input and relevant PDF content
        combined_message = f"Context from PDF:\n\n{relevant_pdf_text}\n\nUser Query: {user_input}"

        llm = GroqAPI(selected_model)
        message.add("user", user_input)
        message.display_chat_history()

        # Stream the response with the context from the PDF
        response = message.display_stream(llm.response_stream(st.session_state.messages))
        message.add("assistant", response)

if __name__ == "__main__":
    main()
