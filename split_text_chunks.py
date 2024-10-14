import time
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_community.vectorstores.faiss import FAISS  # Updated import
import warnings
import os
from document_loader import load_documents

start_time = time.time()
load_start_time = time.time()

print("split_text_chunks.py is being imported")

warnings.filterwarnings("ignore", message='Field "model_name" in HuggingFaceInferenceAPIEmbeddings has conflict with protected namespace "model_".')

def get_pdf_docs(pdf_path):
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""  # Ensure empty string if text is None
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",  # Corrected keyword argument
        chunk_size=2000,  # 1000 characters
        chunk_overlap=200,  # Retrieve 200 characters before ends in order to not miss the meaning
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def save_chunks(chunks, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, chunk in enumerate(chunks):
        with open(os.path.join(output_dir, f"chunk_{i}.txt"), "w", encoding="utf-8") as f:
            f.write(chunk)

    print(f"Saved {len(chunks)} chunks to {output_dir}")

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") # embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")  # Updated to an alternative
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def save_vectorstore(vectorstore, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save FAISS index and metadata
    vectorstore.save_local(output_dir)
    print(f"Vectorstore saved to {output_dir}, number of vectors: {vectorstore.index.ntotal}")

    # If your vectorstore has associated documents, print metadata (if stored)
    if hasattr(vectorstore, 'docs'):
        print(f"Document metadata: {vectorstore.docs[:5]}")  # Print metadata of the first 5 documents

def query_vectorstore(vectorstore, query, embeddings, chat_model, is_document_query=True):
    # Embed the query as a single string
    query_embedding = embeddings.embed_query(query)  # Embed the query text

    if is_document_query:
        # similarity search using FAISS
        results = vectorstore.similarity_search_by_vector(query_embedding)

        # check for results
        if not results:
            print(f"No results found for query '{query}'.")
            return

        # top similar result
        top_result = results[0]

        # use llm to generate summary of the document
        summary = chat_model.answer_question("A003", f"Summarize the following content: {top_result.page_content}")

load_duration = time.time() - load_start_time
print(f"- Loading split_text_chunks.py took {load_duration:.2f} seconds")
