import streamlit as st
import time
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings

from dotenv import load_dotenv
import os
load_dotenv()
groq_api_key = os.getenv('groq_api')

st.title("RAG Doc Assistant")

# Initialize the LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="mixtral-8x7b-32768"  # Updated to a more current model
)

prompt = ChatPromptTemplate.from_template(
    """
    You are a document assistant that helps users find information in a context.
    Please provide the most accurate response based on the context and inputs.
    Only give information that is in the context, not in general.
    
    <context>
    {context}
    </context>
    
    Question: {input}
    """
)

# Function to process the uploaded PDF
def vector_embedding(uploaded_file):
    if "vectors" not in st.session_state:
        try:
            # Save the uploaded file to a temporary location
            with open("temp_uploaded_file.pdf", "wb") as temp_file:
                temp_file.write(uploaded_file.read())
            
            # Initialize Ollama embeddings
            st.session_state.embeddings = OllamaEmbeddings(
                model="nomic-embed-text",
                base_url="http://localhost:11434"  # Default Ollama URL
            )
            
            # Load and process the document
            st.session_state.loader = PyPDFLoader("temp_uploaded_file.pdf")
            st.session_state.docs = st.session_state.loader.load()
            
            # Create chunks
            st.session_state.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            )
            
            # Split documents
            st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
            
            # Create vector store
            with st.spinner("Creating vector embeddings... This may take a few moments."):
                st.session_state.vectors = FAISS.from_documents(
                    st.session_state.final_documents, 
                    st.session_state.embeddings
                )
            
            return True
            
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            return False
            
        finally:
            # Clean up temporary file
            if os.path.exists("temp_uploaded_file.pdf"):
                os.remove("temp_uploaded_file.pdf")

# File uploader for PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Add a reset button
if st.button("Reset"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Application state has been reset!")

# Embedding button
if st.button("Process Document") and uploaded_file:
    success = vector_embedding(uploaded_file)
    if success:
        st.success("Document processed successfully!")

# Input for the question
prompt1 = st.text_input("Enter Your Question About the Document")

if prompt1:
    if "vectors" in st.session_state:
        try:
            with st.spinner("Generating response..."):
                document_chain = create_stuff_documents_chain(llm, prompt)
                retriever = st.session_state.vectors.as_retriever()
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                
                start = time.process_time()
                response = retrieval_chain.invoke({'input': prompt1})
                elapsed_time = time.process_time() - start
                
                st.write(f"Response time: {elapsed_time:.2f} seconds")
                st.write(response['answer'])

                # Show relevant document sections
                with st.expander("Document Similarity Search"):
                    for i, doc in enumerate(response["context"]):
                        st.markdown(f"**Relevant Section {i+1}:**")
                        st.write(doc.page_content)
                        st.divider()
        
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
    else:
        st.warning("Please process the document first.")
