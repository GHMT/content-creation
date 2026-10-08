# Module 7: Enterprise vs. Personal AI Teams

## 📌 Introduction
When you use AI agents on a personal project, the friction is virtually zero. You have the entire architecture in your head, there are no other team members to coordinate with, and you don't have to follow strict repository gatekeepers.

In an **Enterprise Company**, everything changes. You are working with a legacy codebase, strict style guides, CI/CD gates, security compliance, and multiple engineers running their own AI agents simultaneously.

This module details how to scale AI-native workflows to real-world software engineering teams.

---

## 🔑 Key Differences

| Dimension | Personal Project | Enterprise / Team Project |
| :--- | :--- | :--- |
| **Context Size** | Small, easily fits in LLM context. | Massive legacy codebase; RAG & indexing are critical. |
| **Code Ownership** | Shared context; single coder. | Collaborative ownership; strict branch protections. |
| **Rules & Styles** | Loose or ad-hoc formatting. | Rigid linting, formatting rules, architectural boundaries. |
| **Velocity Bottleneck**| Typing and thinking speed. | Coordination, reviews, and regression testing. |
| **Security Risk** | Minimal (local database, personal credentials). | Severe (PII, customer data, leaking proprietary code). |

---

## ⚡ Team Coordination & Conflict Resolution
When multiple developers run autonomous agents, the speed of code output increases exponentially. This causes two main friction points:

### 1. The Merge Conflict Storm
*   **The Issue**: Two developers instruct their respective agents to refactor components. Because agents can edit multiple files in seconds, they submit large PRs that heavily overlap, resulting in massive, hard-to-resolve merge conflicts.
*   **The Solution**:
    - **Micro-Branches**: Keep feature scopes tiny. Create branches for specific tasks, build them, and merge within hours, not weeks.
    - **Continuous Rebasing**: Ensure developers rebase their branches hourly. Agents should be instructed to check for upstream conflicts before editing.

### 2. Standardizing AI Behavior (Shared Rulesets)
*   **The Issue**: Developer A's agent uses tabs and functional React components. Developer B's agent uses spaces and class-based components, leading to formatting wars.
*   **The Solution**:
    - Check team configuration rules (e.g., `.cursorrules` or `.windsurfrules`) directly into the root of the git repository.
    - This forces all team members' agents to adopt identical lint, formatting, and architecture rules.

---

## 🔒 Enterprise Security & Sandboxing
AI agents represent a new attack vector in the enterprise:

1.  **Typo-Squatting / Dependency Attacks**: Agents may hallucinate a helper library that does not exist. Attackers can register a malicious library under that hallucinated name. If the team's build pipeline auto-installs it, they get compromised.
    - *Defense*: Agents must not have permission to add unapproved external dependencies without human override.
2.  **Secret Leakage**: Agents might write temporary API credentials or private keys directly into code files.
    - *Defense*: Run automated pre-commit scanners (like GitGuardian or Trufflehog) to block secrets from being pushed to git.
3.  **Command Execution Safety**: Giving agents terminal write access can lead to destructive commands (e.g. `rm -rf /` or deleting database tables).
    - *Defense*: Agents should run commands inside isolated sandboxes (Docker/VMs) or require explicit human approval for destructive shell statements.

---

## 🧠 Classroom Discussion / Exercise
1.  **Designing Security Rules**: Write a `.cursorrules` snippet that explicitly forbids an agent from installing new npm/pip packages without listing them in a custom approval file.
2.  **The Code Review Dilemma**: VPs of Engineering are seeing PR reviews become a bottleneck. If developers write code in 5 minutes, but human review takes 24 hours, how does the team maintain velocity? How can AI help in the review stage?

---

## 📖 Recommended Reading & Resources
*   *Securing the AI Workspace: Threat Models for Coding Agents*
*   *Git Workflows for Multi-Agent Developer Teams*

---
[Back to Curriculum](file:///Users/maxtomasello/git/own/software-engineering/courses/ai-native-sdlc/curriculum.md)
