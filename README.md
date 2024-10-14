# 🚀 Document-Based Chatbot with LangChain, FAISS, Llama2, and MiniLM 🌟
Welcome to the Document-Based Chatbot project! This chatbot is designed to retrieve and respond to document-based queries, leveraging the power of several cutting-edge technologies:

- LangChain: For conversational logic and orchestration.
- FAISS: For efficient vector-based similarity searches.
- Llama2: As the core language model for natural conversation.
- MiniLM: For generating text embeddings.

## ✨ Features
- ⚡ Real-time querying of document-based knowledge.
- 🔍 Efficient similarity search using FAISS.
- 🤖 Conversational logic orchestration powered by LangChain.
- 🧠 Llama2 fine-tuned language model for natural conversations.
- 🧬MiniLM embeddings for efficient text representation.

## 🛠️ Project Structure
- **`app.py`**: Main script for running the chatbot app.
- **`model.py`**: Defines the language model (**Llama2**) and embedding model (**MiniLM**).
- **`split_text_chunks.py`**: Utility functions for splitting PDF or text documents into chunks and handles the creation and querying of the FAISS vector store.
- **`document_loader.py`**: Manages document loading and processing.
- **`requirements.txt`**: Lists all the dependencies required for the project.

## 🚀 How It Works
1. **Document Ingestion**: Load documents and split them into smaller chunks.
2. **Vector Embedding**: Convert text chunks into embeddings using **MiniLM**.
3. **FAISS Indexing**: Use **FAISS** for fast similarity searches on the embeddings.
4. **Chatbot Interaction**: Handle conversational context and queries with **LangChain**.

## 🌐 Related

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://faiss.ai/)
- [Llama2 GitHub](https://github.com/facebookresearch/llama)
- [MiniLM on Hugging Face](https://huggingface.co/sentence-transformers/MiniLM-L6-v2)
- [Retrieval-Augmented Generation (RAG) Explained](https://medium.com/@dminhk/retrieval-augmented-generation-rag-explained-b1dd89979681)
- [LangChain example](https://medium.com/@bijit211987/llm-powered-applications-building-with-langchain-cad4032d733c)

## 📜 License

This project is licensed under the **MIT License**.
