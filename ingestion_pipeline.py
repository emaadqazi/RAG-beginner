import os 
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma 
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path="docs"):
    """ Load all text files from the /docs directory"""
    print(f"Loading documents from {docs_path}")

    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The directory {docs_path} does not exist. Please create it and add your files.")

    # DirectoryLoader is a LangChain class that scans a folder and loads multiple documents at once into a format LangChain can work with (see documents comment below)
    # path = folder to scan
    # glob="*.txt" -> only load files with specified name. "*" means "any file name", so we are loading all the text files 
    # loader_cls = TextLoader -> how to read each file, TextLoader just reads plain files 
    loader = DirectoryLoader(
        path=docs_path, 
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    if len(documents) == 0:
        raise FileNotFoundError(f"No .txt files found in {docs_path}. Please add documents")
    
    for i, doc in enumerate(documents[:2]): # Show the first 2 documents 
        print(f"\nDocument {i+1}:")
        print(f"    Source {doc.metadata['source']}")
        print(f"    Content length: {len(doc.page_content)} characters")
        print(f"    Content preview: {doc.page_content[:100]}...")
        print(f"    metadata: {doc.metadata}")

# documents = [
#    Document(
#        page_content="Google LLC is an American multinational corporation and technology company focusing on online advertising, search engine technology, cloud computing, computer software, quantum computing, e-commerce, consumer electronics, and artificial intelligence (AI).",
#        metadata={'source': 'docs/google.txt'}
#    ),
#    Document(
#        page_content="Microsoft Corporation is an American multinational corporation and technology conglomerate headquartered in Redmond, Washington.",
#        metadata={'source': 'docs/microsoft.txt'}
#    ),
#    Document(
#        page_content="Nvidia Corporation is an American technology company headquartered in Santa Clara, California.",
#        metadata={'source': 'docs/nvidia.txt'}
#    ),
#    Document(
#        page_content="Space Exploration Technologies Corp., commonly referred to as SpaceX, is an American space technology company headquartered at the Starbase development site in Starbase, Texas.",
#        metadata={'source': 'docs/spacex.txt'}
#    ),
#    Document(
#        page_content="Tesla, Inc. is an American multinational automotive and clean energy company headquartered in Austin, Texas.",
#        metadata={'source': 'docs/tesla.txt'}
#    )
# ]

    return documents

def split_documents(documents, chunk_size=800, chunk_overlap=0):
    """ Split doucments into smaller chunks with overlap"""

    print("Splitting documents into chunks...")
    # Basic chunk splitting methodology - will get more advanced
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = text_splitter.split_documents(documents)

    if chunks:
        for i, chunk in enumerate(chunks[:5]): # Limited to first 5 chunks
            print(f"\n--- Chunk{i+1} ---")
            print(f"Source: {chunk.metadata['source']}")
            print(f"Length: {len(chunk.page_content)} characters")
            print(f"Content:")
            print(chunk.page_content)
            print("-" * 50)

        if len(chunks) > 5:
            print(f"\n... and {len(chunks) - 5} more chunks")

    return chunks 

def main():
    print("Main function")

    # (1) Load the files 
    documents = load_documents("docs")

    chunks = split_documents(documents)

if __name__ == '__main__':
    main()