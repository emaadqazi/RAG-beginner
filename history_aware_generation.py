from dotenv import load_dotenv
from langchain_chroma import Chroma 
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables
load_dotenv()

# Connect to the document database
"""
We need to specify the directory (vector DB) and the embedding models to call the 
Chroma function
"""
persistent_directory = "db/chroma_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

# AI Model
model = ChatOpenAI(model="gpt-4o")

# Array to store our conversations as messages to send to DB
chat_history = []

def ask_question(user_question):
    print(f"\n--- You asked: {user_question} ---")

    # (1) Make the question clear using conversation history
    if chat_history:
        # Ask AI to reformat question into one 
        messages = [
            SystemMessage(content="Given the chat history, rewrite the new question to be standalone and searchable. Just return the rewritten question."),
        ] + chat_history + [
            HumanMessage(content=f"New question: {user_question}")
        ]

        result = model.invoke(messages)
        search_question = result.content.strip()
        print(f"Searching for: {search_question}")
    else: # There is no previous chat history
        search_question = user_question

    # (2) Find the relevant documents
    retriever = db.as_retriever(search_kwargs={"k": 3}) # Top 3 chunks
    docs = retriever.invoke(search_question)

    print(f"Found {len(docs)} relevant documents:")
    for i, doc in enumerate(docs, 1):
        # Show the first 2 lines of each document
        lines = doc.page_content.split('\n')[:2]
        preview = '\n'.join(lines)
        print(f"    Doc {i}: {preview}...")

    # (3) Create the final prompt
    combined_input = f"""Based on the following documents, please answer this question: {user_question}

    Documents:
    {"\n".join([f"- {doc.page_content}" for doc in docs])}

    Please provide a clear, helpful answer using only the information from these documents. If you can't find the answer in the documents, return "I don't have enough information to answer that question based on the provided documents."
    """

    # (4) Get the answer
    messages = [
        SystemMessage(content="You are a helpful assistant that answers questions based on provided documents and conversation history."),
    ] + chat_history + [
        HumanMessage(content=combined_input)
    ]

    result = model.invoke(messages)
    answer = result.content

    # (5) Append the conversation to chat history
    chat_history.append(HumanMessage(HumanMessage(content=user_question)))
    chat_history.append(AIMessage(content=answer))

    print(f"Answer: {answer}")
    return answer

def start_chat():
    print("Ask me question! Type 'quit' to exit.")

    while True:
        question = input("\nYour question:")

        if question.lower() == 'quit':
            print("Exiting...")
            break 

        ask_question(question)

if __name__ == '__main__':
    start_chat()

