import sys
import os
import argparse
from playwright.sync_api import sync_playwright
import pyperclip

# Save the session auth file in the scripts directory, or local directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUTH_FILE = os.path.join(SCRIPT_DIR, "medium_auth.json")

def capture_session():
    """Launches a browser for a one-time manual login to save credentials."""
    print("🚀 Launching browser for authentication...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        context.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
        page = context.new_page()
        
        # Navigate to sign-in page
        page.goto("https://medium.com/m/signin")
        
        print("\n👉 Please log in to Medium in the opened browser window.")
        print("👉 Once logged in and redirected to your homepage, close the browser window.")
        
        # Keep open until the user closes the page or logs in (wait up to 5 minutes)
        try:
            page.wait_for_timeout(300000)
        except Exception:
            pass
            
        # Serialize context state
        context.storage_state(path=AUTH_FILE)
        print(f"\n✅ Session successfully saved to '{AUTH_FILE}'!")
        browser.close()

def publish_draft(markdown_path):
    """Loads the session, copies markdown to the clipboard, and pastes it into the Medium editor."""
    if not os.path.exists(AUTH_FILE):
        print(f"❌ Error: '{AUTH_FILE}' not found. Run with --login first.")
        sys.exit(1)
        
    if not os.path.exists(markdown_path):
        print(f"❌ Error: Markdown file '{markdown_path}' not found.")
        sys.exit(1)
        
    print(f"📖 Reading markdown file: {markdown_path}")
    with open(markdown_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Copy content to system clipboard
    print("📋 Copying content to clipboard...")
    pyperclip.copy(content)
    
    print("🚀 Opening browser to create draft...")
    with sync_playwright() as p:
        # Run headed so you can watch the magic, or change to headless=True for background runs
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # Load the authenticated storage state
        context = browser.new_context(
            storage_state=AUTH_FILE,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        context.add_init_script("delete Object.getPrototypeOf(navigator).webdriver;")
        page = context.new_page()
        
        # Navigate to New Story page
        page.goto("https://medium.com/new-story")
        page.wait_for_load_state("networkidle")
        
        # Check if login was successful by validating url
        if "signin" in page.url:
            print("❌ Session expired. Please run the script with --login to re-authenticate.")
            browser.close()
            sys.exit(1)
            
        print("✍️ Pasting article contents...")
        # Focus on the Title input field
        page.focus("h3[data-placeholder='Title']")
        
        # Paste the content (using Cmd+V for macOS, Ctrl+V for other OS)
        if sys.platform == "darwin":
            page.keyboard.press("Meta+V")
        else:
            page.keyboard.press("Control+V")
            
        # Wait a moment for Medium to parse the pasted content
        page.wait_for_timeout(4000)
        
        print("💾 Saving as draft...")
        page.wait_for_load_state("networkidle")
        
        # We stop at draft creation to let you review the formatting and manually hit publish
        print(f"\n🎉 Success! Your draft is ready on Medium at: {page.url}")
        print("Close the browser when you are done.")
        page.wait_for_timeout(10000)
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Medium drafts using Playwright.")
    parser.add_argument("--login", action="store_true", help="Log in manually to save session credentials.")
    parser.add_argument("--publish", type=str, help="Path to the markdown file to import.")
    
    args = parser.parse_args()
    
    if args.login:
        capture_session()
    elif args.publish:
        publish_draft(args.publish)
    else:
        parser.print_help()
