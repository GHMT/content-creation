# Chapter 5: Knowledge Retrieval

This chapter focuses on feeding agents correct, context-rich factual knowledge from corporate databases, wikis, and graph structures.

---

## 🔑 Core Lessons & Topics

### 1. Standard Vector RAG (Static Content Integration)
*   **Concept**: Chunking text documents, generating vector embeddings, and retrieving relevant chunks via cosine similarity to answer user questions.
*   **Use Cases**: Standard corporate Help Centers, PDF manuals, standard developer wikis, and API documentation.
*   **Best Practice**: Use semantic chunking, metadata filtering (e.g. version numbers, product tags), and re-ranking models (like Cohere ReRank) to surface the most relevant text chunks.

### 2. GraphRAG
*   **Concept**: Overlaying a Knowledge Graph (nodes representing entities, edges representing relationships) on top of raw vector documents.
*   **Why it's needed**: Standard vector RAG fails at global questions (e.g., *"What are the common problems mentioned across all customer support tickets this month?"*). GraphRAG enables global summarization and entity connection.
*   **Best Practice**: Extract entities and relationships using LLM prompts during the ingestion step. Store the graph in a graph database (like Neo4j) and query it in tandem with vector searches.

---

## 🛠️ Chapter Exercise
*   **Activity**: Create a simple entity-relationship graph (nodes, relationships) modeling a developer team organization chart, and show how a GraphRAG system would trace dependencies to answer: *"Who is the ultimate decision maker for database changes?"*
