# Module 2: The Modern AI Developer Toolbelt & Agent Skills

## 📌 Introduction
Not all AI coding assistants are created equal. Using a chat prompt to fix a minor syntax error is like using a sledgehammer to crack a nut. Conversely, using inline autocomplete to build a whole microservice is slow and frustrating.

To be an effective AI-native engineer, you must understand the **Spectrum of AI Developer Tools**, how **Agent Skills** extend the capacity of autonomous agents, and how to select the appropriate interface for the task at hand.

---

## 🔑 Key Concepts

### 1. The Spectrum of AI Assistance

```
[ LOW AUTONOMY ] ──────────────────────────────────────────► [ HIGH AUTONOMY ]
  Level 1: Autocomplete      Level 2: Chat & Edit        Level 3: Agentic Workflows
  (GitHub Copilot inline)    (Cursor Chat, Claude Dev)   (Cursor Composer, Antigravity)
```

#### 🔹 Level 1: Inline Autocomplete (Ghost Text)
*   **Best for**: Boilerplate, completing repetitive arrays/structures, writing simple functions.
*   **Limitations**: Lacks awareness of system architecture; can only edit at your cursor position.

#### 🔹 Level 2: Chat-assisted Editing (Sidebar Chat)
*   **Best for**: Exploring new libraries, explaining legacy code, converting code between languages.
*   **Limitations**: Edits are usually confined to a single file; requires manual acceptance.

#### 🔹 Level 3: Agentic Workflows (Multi-File Agents)
*   **Best for**: Creating new features, refactoring database schemas, upgrading package dependencies.
*   **Capabilities**: Equipped with terminal access, file system tools, and workspace search.

---

## 🛠️ What are Agent Skills?
When an AI agent is running autonomously (Level 3), it cannot solve complex domain-specific tasks using raw text generation alone. Instead, it relies on **Agent Skills**.

An **Agent Skill** is a packaged bundle of instructions, helper scripts, and API clients that expose specific tools to the agent.
*   **How they work**: The developer defines a skill schema that explains to the agent:
    1.  *What* the skill does (metadata).
    2.  *How* to run it (executable scripts/APIs).
    3.  *What* inputs/outputs it expects.
*   **Examples of Skills**:
    - `dbsnp-database`: A skill allowing an agent to query genetic variants.
    - `chrome-devtools`: A skill allowing an agent to open a browser, click buttons, and inspect console logs to troubleshoot frontend code.
    - `spin-off-ecosystem-planner`: An instruction-only skill that guides an agent to output structured funnel plans in a specific workspace path.

---

## ⚙️ Standardizing Agent Behavior with `.cursorrules`
You can program your IDE's AI behavior using configuration rules (e.g., `.cursorrules`, `.windsurfrules`). These files live in the root of the repository and tell the agent how to behave, what code patterns to use, what style guides to follow, and how to utilize custom skills.

### Example Rules Snippet:
```markdown
# Agent Execution Guidelines
- You have access to custom bash tools. Always run `npm run lint` after modifying a file.
- Before proposing any file changes, read the appropriate blueprint in `/plans`.
- If you need to plan a monetization funnel, trigger the custom `spin-off-ecosystem-planner` skill.
- Never use unverified third-party libraries; stick to the approved dependencies in `package.json`.
```

---

## 🧠 Codebase Context: How AI "Sees" Your Code
AI tools cannot process millions of lines of code in a single prompt due to context window limits. Instead, they use several techniques to build local context:

1.  **Vector Embeddings & RAG**: The IDE indexer scans your codebase, splits code files into chunks, and stores mathematical representations (embeddings) of their semantic meaning. When you ask a question, it fetches the most relevant code chunks.
2.  **LSP (Language Server Protocol) Integration**: Modern IDEs use compiler information (definitions, references, hover cards) to feed structured context to the LLM.
3.  **File Context Mentions**: Using `@filename` or `@symbol` syntax in chat to explicitly inject critical files or functions into the LLM context.

---

## 💻 Practical Exercise: Mastering Context Injection
1.  **Open an IDE with codebase indexing** (e.g. Cursor, VS Code with Copilot Workspace).
2.  **Experiment with context tagging**:
    *   Ask the chat: *"How is authentication handled?"* without tagging files. Observe the generic response.
    *   Repeat the query, tagging the specific auth module using `@auth.ts` or `@auth_service`. Note the increase in accuracy and specificity.
3.  **Use an Agentic tool**: Propose a multi-file change (e.g., *"Add a logging middleware to all server routes"*) and watch the agent create, edit, and lint the files.

---

## 📖 Recommended Reading & Resources
*   *LSP and AI: Bridging the Gap between Compilers and Language Models*
*   *Configuring your codebase for optimal IDE indexing (.gitignore and search exclude rules)*

---
[Back to Curriculum](file:///Users/maxtomasello/git/own/software-engineering/courses/ai-native-sdlc/curriculum.md) | [Next Module: AI-Native Planning & Spec-Driven Development](file:///Users/maxtomasello/git/own/software-engineering/courses/ai-native-sdlc/modules/module-3-planning.md)
