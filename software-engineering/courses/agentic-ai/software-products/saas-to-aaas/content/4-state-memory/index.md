# Chapter 4: State & Memory Systems

This chapter addresses the critical architectures for managing state, session history, persistent memories, and multi-tenant isolation in agentic backends.

---

## 🔑 Core Lessons & Topics

### 1. Short-Term Memory (Session State)
*   **Concept**: Storing the current conversation thread history.
*   **Best Practice**: Use sliding-window context management. When a conversation exceeds the model's token limits, prune historical messages, summarize the older parts of the thread, or selectively keep only high-value system instructions.

### 2. Long-Term Memory (Persistent Context)
*   **Concept**: Saving user preferences, semantic facts, and past task results across sessions.
*   **Architectural Model**: 
    - **Vector Memory**: Unstructured conversation highlights stored in a vector database for semantic retrieval.
    - **Relational Memory**: Structured database tables tracking explicit user profiles, configuration properties, and static key-value states.
    - *Reference*: Review [From RAG to Memory Systems](file:///Users/maxtomasello/git/own/software-engineering/courses/saas-to-aaas/references/README.md) for a detailed look at stateful AI architectures.

### 3. Multi-Tenant Agentic Architecture
*   **Concept**: Building a shared application environment where multiple corporate customers (tenants) run agents, without any risk of data leakage between tenants.
*   **Best Practice**:
    - Enforce row-level security (RLS) or tenant isolation keys in all database/vector queries.
    - Inject the tenant ID into the system prompt context programmatically before any tool calls run.
    - Isolate vector namespaces or databases per tenant to prevent cross-tenant semantic retrieval.

---

## 🛠️ Chapter Exercise
*   **Activity**: Design a database schema for an agent memory system that separates: (1) active session state, (2) long-term user preferences (relational), and (3) episodic memory snippets (vector/semantic).
