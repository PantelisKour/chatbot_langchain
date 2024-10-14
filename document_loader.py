import time
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from pydantic.v1.utils import path_type

start_time = time.time()
load_start_time = time.time()

print("document_loader.py is being imported")

DATA_PATH = "FILE_PATH"

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf",loader_cls=UnstructuredFileLoader)
    documents = loader.load()
    return documents

load_duration = time.time() - load_start_time
print(f"- Loading document_loader.py took {load_duration:.2f} seconds")
