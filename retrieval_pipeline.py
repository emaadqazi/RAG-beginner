from langchain_chroma import Chroma 
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv 

load_dotenv()

persistent_directory = "db/chroma_db"

# Load the embeddings and vector store
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small") # using the same model we used in ingestion_pipeline

# Providing directory to Chroma, the model, and then the algorithm we are going to use in retrieval
db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space": "cosine"}
)

query = "In what year did Tesla begin production of the Roadster"

# We are trying to retrieve the top 3 chunks
retriever = db.as_retriever(search_kwargs={"k": 5}) 

relevant_docs = retriever.invoke(query)

print(f"User Query: {query}")
print("-- Context --")
for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:\n{doc.page_content}\n")