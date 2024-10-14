import os
import time
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables import RunnableWithMessageHistory
from dotenv import load_dotenv
from document_loader import load_documents
from langchain.chains.combine_documents import create_stuff_documents_chain

start_time = time.time()
load_start_time = time.time()

print("model.py is being imported")

documents = load_documents()
pdf_path = documents[0].metadata['source']

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "<api_key>"


class ChatModel:
    def __init__(self):
        self.llm = Ollama(
            model="llama2", callbacks=[StreamingStdOutCallbackHandler()]
        )

        # define prompts
        prompt_llm = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an assistant for question-answering tasks. "
                           "Answer all the question at your best."),
                MessagesPlaceholder(variable_name="messages_llm"),
            ]
        )

        prompt_docs = ChatPromptTemplate.from_messages(
            [
                ("system", "You are assisting with document-related queries. "
                           "Use the document-based context to provide accurate information. "
                           "If unsure, state that the answer is not available."),
                MessagesPlaceholder(variable_name="messages_docs"),
            ]
        )

        # Create chains
        chain_llm = prompt_llm | self.llm
        chain_docs = prompt_docs | self.llm

        self.store_llm = {}
        self.store_docs = {}

        # Get session histories
        self.get_session_history_llm = lambda session_id: self.store_llm.setdefault(session_id,
                                                                                    InMemoryChatMessageHistory())
        self.get_session_history_docs = lambda session_id: self.store_docs.setdefault(session_id,
                                                                                      InMemoryChatMessageHistory())

        # Chains with message histories
        self.with_message_history_llm = RunnableWithMessageHistory(chain_llm, self.get_session_history_llm)
        self.with_message_history_docs = RunnableWithMessageHistory(chain_docs, self.get_session_history_docs)

    def answer_question(self, session_id: str, user_input: str, is_document_query=False):
        if is_document_query:
            response = self.with_message_history_docs.invoke(
                {
                    "messages": [HumanMessage(content=user_input)]
                },
                config = {"configurable": {"session_id": "A003"}}
            )
        else:
            response = self.with_message_history_llm.invoke(
                {
                    "messages": [HumanMessage(content=user_input)]
                },
                config = {"configurable": {"session_id": "A002"}}
            )
        return response

load_duration = time.time() - load_start_time
print(f"- Loading model.py took {load_duration:.2f} seconds")
