# RAG System From Scratch

## Overview

This project is a beginner-friendly implementation of a Retrieval-Augmented Generation (RAG) system built from scratch.

The goal is to understand how a RAG pipeline works end to end, from loading documents into a vector database to retrieving relevant context and generating answers with an LLM.

## What This Project Covers

This repository explores the core stages of a RAG system:

- Document ingestion and preprocessing
- Chunk splitting for better retrieval
- Embedding generation
- Vector storage with Chroma
- Document retrieval
- History-aware question answering with an LLM

## Why RAG

Large language models are powerful, but they do not automatically know your private documents or project-specific knowledge.

RAG solves this by combining:

- Retrieval, which finds relevant information from your documents
- Generation, which uses an LLM to answer questions using that retrieved context

This makes answers more grounded, more relevant, and easier to control.

## Project Structure

- `ingestion_pipeline.py` loads documents, splits them into chunks, and stores embeddings in Chroma.
- `retrieval_pipeline.py` tests retrieval by querying the vector database and printing relevant chunks.
- `history_aware_generation.py` uses chat history plus retrieved documents to answer questions in a conversational way.
- `docs/` contains the source documents used to build the knowledge base.
- `db/chroma_db/` stores the persistent Chroma vector database.

## How It Works

The pipeline follows a simple workflow:

1. Load documents from the `docs/` folder.
2. Split the documents into smaller chunks.
3. Convert each chunk into embeddings.
4. Store the embeddings in Chroma.
5. Accept a user question.
6. Retrieve the most relevant chunks.
7. Send the question and context to the LLM.
8. Return an answer grounded in the documents.

## History-Aware Generation

The `history_aware_generation.py` script improves retrieval by rewriting follow-up questions into standalone questions before searching the vector database.

For example, if the user asks:

- Who founded it?
- When was it created?

the model uses the conversation history to interpret what "it" refers to before retrieving relevant context.

## Learning Goals

This project is meant to help understand:

- How chunk size affects retrieval quality
- Why embedding models matter
- How vector search works
- How LLMs can be grounded in external documents
- How chat history can improve question answering

## Technologies Used

- Python
- LangChain
- Chroma
- OpenAI embeddings
- OpenAI chat models
- dotenv for environment variable management

## Future Improvements

Possible next steps for this project include:

- Adding similarity score thresholds for answer confidence
- Improving chunking strategy and metadata handling
- Adding source citations to responses
- Supporting more documents and larger datasets
- Comparing different embedding and retrieval strategies
- Adding a web UI for easier interaction