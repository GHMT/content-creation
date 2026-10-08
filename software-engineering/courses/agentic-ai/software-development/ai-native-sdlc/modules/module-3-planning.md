# Module 3: AI-Native Planning & Spec-Driven Development

## 📌 Introduction
When developers get access to agentic AI tools, the temptation is to immediately prompt: *"Build me a dashboard with authentication and a database."* 

This approach almost always leads to **architectural drift**, bugs, and massive context exhaustion. The agent writes random code, hits errors, tries to fix them with more random code, and eventually runs out of context space or makes the codebase unmaintainable.

To build complex systems with AI, you must adopt **Spec-Driven Development (SDD)**. You plan first, write a blueprint, align on details, and then let the agent execute.

---

## 🔑 Key Concepts

### 1. The Cost of Ambiguity
AI models are statistical engines; when presented with ambiguity, they guess. If they guess incorrectly, they build a tower of code on a weak foundation. Spec-Driven Development eliminates guesswork by documenting constraints *before* code is generated.

### 2. The Markdown Blueprint Pattern
A Markdown Blueprint is a structured, human-readable and machine-understandable specification file. It is written in plain Markdown and lives inside the repository (often in a `.system` or `.plans` folder, or as an artifact).

A great Blueprint contains:
*   **Goal & Scope**: What are we building, and what is explicitly *out of scope*?
*   **Architectural Decisions**: Tech stack, patterns (e.g., repository pattern, custom hooks), security models.
*   **Schema & API Contracts**: JSON schemas, database migration layouts, function signatures.
*   **File-by-File Proposed Changes**: Explicit mapping of what files will be created (`[NEW]`), modified (`[MODIFY]`), or deleted (`[DELETE]`).
*   **Verification Strategy**: How will we *prove* the implementation works? (Unit tests, integration tests, E2E flows).

---

## 🗺️ The Spec-Driven SDLC Loop

```mermaid
flowchart TD
    A[Define Goals & Requirements] --> B[Write Markdown Blueprint]
    B --> C{Review Spec with Human/AI}
    C -->|Revisions Needed| B
    C -->|Approved| D[Let Agent Execute Spec]
    D --> E[Continuous Verification (Test Loop)]
    E --> F[Merge & Ship]
```

### Why this works:
*   **Separation of concerns**: You separate *design thinking* from *implementation mechanics*.
*   **Validation**: It's much cheaper to catch a design flaw in a markdown file than to refactor 1,000 lines of generated code across 15 files.
*   **State Tracking**: The agent can read the spec file to maintain focus, avoiding "context drift" where it forgets the original requirements midway.

---

## 📝 Anatomy of a Blueprint (Template)

Below is the standard layout you should teach your teams to use:

```markdown
# Blueprint: [Feature Name]

## 1. Goal
Short explanation of the user value and technical requirement.

## 2. Architectural Design
- Database modifications (DDL statements)
- API endpoint specifications (routes, methods, payloads)
- State management strategy

## 3. Implementation Checklist
- [ ] Create database schema `db/migrations/XXXX_add_users.sql`
- [ ] Create utility functions in `src/utils/crypto.ts`
- [ ] Implement backend controller in `src/controllers/auth.ts`
- [ ] Build UI component in `src/components/LoginForm.tsx`

## 4. Verification Plan
- Unit tests to run: `npm test utils/crypto`
- Integration tests: Verify `/api/auth/login` returns 200 on valid credentials.
```

---

## 💻 Classroom Exercise: Writing a Blueprint
1.  **Select a simple feature**: *"Create a user profile editing page with profile picture uploads."*
2.  **Draft a spec**: Before writing any code, draft a Markdown Blueprint detailing the API endpoints (`PATCH /api/users/profile`), database columns to add, and component layout.
3.  **Feed the spec to your AI agent**: Instruct the agent: *"Read this blueprint and implement it step-by-step. Do not deviate from the blueprint. Verify each step as you complete it."*
4.  **Compare**: Note how much faster and cleaner the agent implements the feature compared to a free-form chat prompt.

---

## 📖 Recommended Reading & Resources
*   *Pragmatic Specification: Writing Docs that Computers Can Read*
*   *Designing Executable Blueprints for Autonomous Agents*

---
[Back to Curriculum](file:///Users/maxtomasello/git/own/software-engineering/courses/ai-native-sdlc/curriculum.md) | [Next Module: Writing Code for and with AI](file:///Users/maxtomasello/git/own/software-engineering/courses/ai-native-sdlc/modules/module-4-development.md)
