# ⚡ Agentic AI Hub - Scripts & Automation

This directory contains utility scripts for managing, exporting, and programmatically publishing content generated within **The Agentic AI Hub**.

---

## ✍️ Medium Publishing Automation

Due to Medium closing its public API for new integration tokens, we leverage a browser automation script via **Playwright** to create story drafts directly from local Markdown files.

### 1. Prerequisites
Install the required Python dependencies:

```bash
pip install playwright pyperclip
playwright install
```

*   `playwright`: Controls the headless/headed browser instance.
*   `pyperclip`: Safely copies markdown content to your system clipboard so Playwright can paste it natively into Medium's editor.

### 2. Usage Instructions

#### Step 1: Capture Your Authentication Session
Run the login flag. A browser window will open. Sign in to your Medium account using your preferred method (Google, email link, Apple, etc.):

```bash
python3 scripts/publish_to_medium.py --login
```

Once logged in and redirected to your homepage, close the browser window. A `medium_auth.json` file will be generated in the `scripts/` directory containing your session cookies.
> [!IMPORTANT]
> **Keep your auth file secure.** Do not check `medium_auth.json` into version control. It is automatically excluded if you have a `.gitignore` active.

#### Step 2: Publish a Markdown Draft
To publish any markdown manuscript in the blogs folder (e.g. Article 1 of Module 2):

```bash
python3 scripts/publish_to_medium.py --publish "artifacts/blogs/02-leveraging-large-language-models-llms-for-agentic-ai/01-laying-the-groundwork-an-introduction-to-early-natural-language-processing/01-laying-the-groundwork-an-introduction-to-early-natural-language-processing.md"
```

The script will launch the browser, load your active session, open the editor, copy the markdown file to your clipboard, and paste it natively. You can inspect formatting, add metadata/tags, and manually submit the draft.
