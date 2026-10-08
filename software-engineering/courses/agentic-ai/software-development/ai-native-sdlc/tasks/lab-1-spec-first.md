# Lab 1: Spec-First Feature Implementation

## 🎯 Learning Objectives
*   Write an unambiguous Markdown Blueprint for a new feature.
*   Guide an AI coding agent to implement the feature across multiple files without architectural drift.
*   Enforce coding conventions through the specification document.

---

## 🛠️ The Scenario
You are building a **User Registration API**. Currently, the registration endpoint accepts any password. You need to add a secure **Password Strength Validator** utility and integrate it into your authentication service. 

Instead of prompting: *"Hey AI, make my password registration secure,"* you will write a strict technical blueprint and guide the AI to implement it.

---

## 📝 Part 1: Write Your Blueprint
Create a file named `spec_password_validation.md` inside your repository's scratch or plans folder. Write the blueprint using the following template:

```markdown
# Blueprint: Password Strength Validation

## 1. Goal
Add a robust password strength validator to the registration flow. Passwords must be at least 8 characters, contain a number, an uppercase letter, and a special character.

## 2. Technical Changes
- **New File**: `src/utils/passwordValidator.ts`
  - Export a function `validatePassword(password: string): { isValid: boolean; errors: string[] }`.
- **Modified File**: `src/services/userService.ts`
  - Import `validatePassword`.
  - In the `registerUser` function, call `validatePassword` before saving the user. If validation fails, return/throw a 400 Bad Request error containing the list of errors.

## 3. Verification Plan
- Unit tests to run: `npm test passwordValidator`
- Integration tests: Send a `POST /api/register` request with an insecure password and verify it fails with HTTP 400 and validation error messages.
```

---

## 🤖 Part 2: Execute the Plan with the Agent
1.  Open your IDE chat or agentic composer.
2.  Provide the blueprint as context:
    ```
    "I have written a technical specification at @spec_password_validation.md. Please read the file and implement the password strength validator utility and integration step-by-step. Do not make any changes outside this blueprint."
    ```
3.  Monitor the agent's edits. If it modifies unrelated files or shortcuts the requirements, stop the agent and point it back to the blueprint.

---

## 🔍 Part 3: Verify the Output
1.  Run the tests as defined in the **Verification Plan**.
2.  Verify compilation: Ensure there are no TypeScript compiler errors or linter warnings.
3.  Perform a manual review of the generated files to check readability, comment headers, and edge-case handling.

---

## 💡 Lab Reflection Questions
*   How did having a blueprint affect the number of iteration rounds needed to get the code right?
*   If you had asked the agent to write the code *without* the blueprint, what architecture decisions would it have had to guess?
