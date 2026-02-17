# modules/browser_controller.py
from playwright.sync_api import sync_playwright
import urllib.parse


class BrowserController:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        print("[Browser] Ready")

    # ==========================================
    # MAIN ROUTER
    # ==========================================
    def handle_command(self, spoken_text: str) -> bool:
        text = spoken_text.lower().strip()

        # --- GOOGLE SEARCH ---
        if text.startswith("google ") or text.startswith("search for ") or text.startswith("look up "):
            return self.google_search(text)

        # --- STEP 4 COMMANDS ---
        if text.startswith("next page"):
            return self.next_page()

        if text.startswith("click"):
            return self.click_result(text)

        if text.startswith("scroll down"):
            self.page.mouse.wheel(0, 900)
            return True

        if text.startswith("scroll up"):
            self.page.mouse.wheel(0, -900)
            return True

        if text.startswith("zoom in"):
            self.page.evaluate("document.body.style.zoom = '110%'")
            return True

        if text.startswith("zoom out"):
            self.page.evaluate("document.body.style.zoom = '90%'")
            return True

        return False

    # ==========================================
    # GOOGLE SEARCH (stateful)
    # ==========================================
    def google_search(self, spoken_text: str) -> bool:
        words = spoken_text.split()

        if not words:
            return False

        if words[0] == "google":
            query = " ".join(words[1:])
        elif spoken_text.startswith("search for "):
            query = spoken_text.replace("search for ", "", 1)
        elif spoken_text.startswith("look up "):
            query = spoken_text.replace("look up ", "", 1)
        else:
            return False

        if not query:
            print("[Browser] No search query detected.")
            return False

        print(f"[Browser] Google searching: {query}")
        encoded = urllib.parse.quote_plus(query)
        self.page.goto(f"https://www.google.com/search?q={encoded}")
        return True

    # ==========================================
    # NEXT PAGE
    # ==========================================
    def next_page(self) -> bool:
        url = self.page.url

        if "google.com/search" in url:
            try:
                self.page.click("a#pnnext")
                print("[Browser] Next page")
                return True
            except:
                print("[Browser] Next button not found")
                return False

        # fallback scroll
        self.page.mouse.wheel(0, 1200)
        return True

    # ==========================================
    # CLICK RESULT
    # ==========================================
    def click_result(self, text: str) -> bool:
        words = text.split()

        if "first" in words:
            idx = 0
        elif "second" in words:
            idx = 1
        elif "third" in words:
            idx = 2
        else:
            idx = 0

        url = self.page.url

        # Google results
        if "google.com/search" in url:
            results = self.page.query_selector_all("h3")
            if len(results) > idx:
                results[idx].click()
                print(f"[Browser] Clicked result {idx+1}")
                return True

        # generic fallback
        links = self.page.query_selector_all("a")
        if len(links) > idx:
            links[idx].click()
            return True

        return False
