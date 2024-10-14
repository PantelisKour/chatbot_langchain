Document-Based Chatbot with LangChain, FAISS, Llama2, MiniLM, and Streamlit
This project showcases the development of a chatbot designed to retrieve and respond to document-based queries. The chatbot is powered by LangChain for conversational logic, FAISS for vector-based similarity searches, Llama2 as the core language model, and MiniLM for embedding generation. The application is deployed using Streamlit to create an interactive and user-friendly interface.

Features
Real-time querying of document-based knowledge.
Efficient similarity search using FAISS.
Conversational logic orchestration powered by LangChain.
Llama2 fine-tuned language model for handling natural conversations.
MiniLM embeddings for efficient text representation in a lower-dimensional space.

Project Structure
app.py: Main script for running the chatbot app.
model.py: Script that defines the language model (Llama2) and embedding model (MiniLM).
split_text_chunks.py: Utility functions for splitting PDF or text documents into chunks, also handles creation and querying of the FAISS vector store.
document_loader.py: Handles document loading and processing.
requirements.txt: Lists all the dependencies required for the project.
