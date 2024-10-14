from model import ChatModel
import split_text_chunks
from document_loader import load_documents

def main():
    chat_model = ChatModel()

    documents = load_documents()

    if not documents:
        print("No documents found")
        return

    pdf_path = documents[0].metadata['source']

    # extract and split text
    raw_text = split_text_chunks.get_pdf_docs(pdf_path)
    text_chunks = split_text_chunks.get_text_chunks(raw_text)

    # save chunks
    output_dir = "chunks"
    split_text_chunks.save_chunks(text_chunks, output_dir)

    embeddings = split_text_chunks.HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # create vector db and save vectors
    vectorstore_dir = "faiss_index"
    vectorstore = split_text_chunks.get_vectorstore(text_chunks)
    split_text_chunks.save_vectorstore(vectorstore, vectorstore_dir)
    #
    # # Query vectorstore for a sample query
    # sample_query = "What is the document about?"
    # split_text_chunks.query_vectorstore(vectorstore, sample_query, embeddings, chat_model)

    print("To chat with documents (doc), in order to chat with llm just ask what do you want")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "bye":
            print("Assistant: Goodbye!")
            break

        if user_input.startswith("doc"):
            query = input()
            split_text_chunks.query_vectorstore(vectorstore, query, embeddings, chat_model, is_document_query=True)
        else:
            response = chat_model.answer_question("A002", user_input, is_document_query=False)

if __name__ == "__main__":
    main()