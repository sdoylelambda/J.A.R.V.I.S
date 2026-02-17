from queue import Queue
from playwright.sync_api import Playwright, sync_playwright
from queue import Queue


class BrowserController:
    def __init__(self):
        self.queue = Queue()
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def process_queue(self):
        while True:
            text = self.queue.get()
            try:
                self.handle_command(text)
            except Exception as e:
                print(f"[BrowserController Error]: {e}")
            self.queue.task_done()










# from playwright.sync_api import sync_playwright
# import urllib.parse
# from queue import Queue
# import threading
# import time
#
#
# class BrowserController:
#     def __init__(self, command_queue: Queue):
#         self.queue = command_queue
#
#         # Start Playwright
#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(headless=False)
#         self.context = self.browser.new_context()
#         self.page = self.context.new_page()
#
#         # Start background thread to process commands
#         self.thread = threading.Thread(target=self._process_queue, daemon=True)
#         self.thread.start()
#
#     # -----------------------------
#     # Public command handler
#     # -----------------------------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower().strip()
#         # Only enqueue browser triggers
#         self.queue.put(spoken_text)
#         return True
#
#     # -----------------------------
#     # Background thread
#     # -----------------------------
#     def _process_queue(self):
#         while True:
#             try:
#                 command = self.queue.get(timeout=0.1)
#             except:
#                 time.sleep(0.01)
#                 continue
#
#             if not command:
#                 continue
#
#             # Google search
#             if command.startswith(("search for ", "google ", "search google for ", "look up ")):
#                 self._handle_search(command)
#                 continue
#
#             # Navigation
#             if command in ["go back", "back"]:
#                 self.page.go_back()
#                 continue
#
#             if command in ["go forward", "forward"]:
#                 self.page.go_forward()
#                 continue
#
#             if command in ["refresh", "reload"]:
#                 self.page.reload()
#                 continue
#
#             if command in ["scroll down"]:
#                 self.page.mouse.wheel(0, 800)
#                 continue
#
#             if command in ["scroll up"]:
#                 self.page.mouse.wheel(0, -800)
#                 continue
#
#             if command in ["zoom in"]:
#                 self.page.evaluate("document.body.style.zoom = '110%'")
#                 continue
#
#             if command in ["zoom out"]:
#                 self.page.evaluate("document.body.style.zoom = '90%'")
#                 continue
#
#             if command in ["next page"]:
#                 self._handle_next_page()
#                 continue
#
#             if command.startswith("click"):
#                 self._handle_click(command)
#                 continue
#
#             if command in ["play video"]:
#                 self._handle_youtube_play()
#                 continue
#
#             # Unrecognized commands are silently ignored in browser queue
#
#             time.sleep(0.01)
#
#     # -----------------------------
#     # Private helpers
#     # -----------------------------
#     def _handle_search(self, text):
#         query = (
#             text.replace("search google for ", "")
#                 .replace("search for ", "")
#                 .replace("google ", "")
#                 .replace("look up ", "")
#         )
#         if query:
#             encoded = urllib.parse.quote_plus(query)
#             self.page.goto(f"https://www.google.com/search?q={encoded}")
#
#     def _handle_next_page(self):
#         url = self.page.url
#         if "google.com/search" in url:
#             try:
#                 self.page.click("a#pnnext")
#             except:
#                 self.page.mouse.wheel(0, 1000)
#         else:
#             self.page.mouse.wheel(0, 1000)
#
#     def _handle_click(self, command):
#         words = command.split()
#         if "first" in words:
#             index = 0
#         elif "second" in words:
#             index = 1
#         elif "third" in words:
#             index = 2
#         else:
#             return
#
#         url = self.page.url
#
#         # Google results
#         if "google.com/search" in url:
#             results = self.page.query_selector_all("h3")
#             if len(results) > index:
#                 results[index].click()
#                 return
#
#         # GitHub repos
#         if "github.com" in url:
#             repos = self.page.query_selector_all("a.v-align-middle")
#             if len(repos) > index:
#                 repos[index].click()
#                 return
#
#         # Generic links
#         links = self.page.query_selector_all("a")
#         if len(links) > index:
#             links[index].click()
#             return
#
#     def _handle_youtube_play(self):
#         url = self.page.url
#         if "youtube.com/watch" in url:
#             self.page.keyboard.press("k")
#             return
#         if "youtube.com/results" in url:
#             videos = self.page.query_selector_all("a#video-title")
#             if videos:
#                 videos[0].click()
#                 return






# from playwright.sync_api import sync_playwright
# import urllib.parse
# import queue
# import threading
# import time
#
#
# class BrowserController:
#     def __init__(self, browser_queue: queue.Queue = None):
#         self.browser_queue = browser_queue or queue.Queue()
#         self.playwright = None
#         self.browser = None
#         self.context = None
#         self.page = None
#
#         # Start Playwright on the main thread
#         self._start_browser()
#
#         # Start recurring queue processor
#         threading.Timer(0.05, self._process_queue).start()
#
#     # -----------------------------
#     # Playwright Initialization
#     # -----------------------------
#     def _start_browser(self):
#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(headless=False)
#         self.context = self.browser.new_context()
#         self.page = self.context.new_page()
#
#     # -----------------------------
#     # Queue Processor
#     # -----------------------------
#     def _process_queue(self):
#         try:
#             while not self.browser_queue.empty():
#                 command = self.browser_queue.get_nowait()
#                 self._execute_command(command)
#         except queue.Empty:
#             pass
#         finally:
#             # Re-run every 50ms
#             threading.Timer(0.05, self._process_queue).start()
#
#     # -----------------------------
#     # Public queue interface
#     # -----------------------------
#     def queue_command(self, text: str):
#         self.browser_queue.put(text)
#
#     # -----------------------------
#     # Execute command on browser
#     # -----------------------------
#     def _execute_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower().strip()
#         print(f"[BrowserController] Executing: {spoken_text}")
#
#         # 🔎 SEARCH
#         if spoken_text.startswith(
#             ("search for ", "google ", "search google for ", "look up ")
#         ):
#             return self._handle_search(spoken_text)
#
#         # 🌍 NAVIGATION
#         if spoken_text in ["go back", "back"]:
#             self.page.go_back()
#             return True
#         if spoken_text in ["go forward", "forward"]:
#             self.page.go_forward()
#             return True
#         if spoken_text in ["refresh", "reload"]:
#             self.page.reload()
#             return True
#         if spoken_text in ["scroll down"]:
#             self.page.mouse.wheel(0, 800)
#             return True
#         if spoken_text in ["scroll up"]:
#             self.page.mouse.wheel(0, -800)
#             return True
#         if spoken_text in ["zoom in"]:
#             self.page.evaluate("document.body.style.zoom = '110%'")
#             return True
#         if spoken_text in ["zoom out"]:
#             self.page.evaluate("document.body.style.zoom = '90%'")
#             return True
#         if spoken_text in ["next page"]:
#             return self._handle_next_page()
#
#         # 🖱 SMART CLICK
#         if spoken_text.startswith("click"):
#             return self._handle_click(spoken_text)
#
#         if spoken_text in ["play video"]:
#             return self._handle_youtube_play()
#
#         return False
#
#     # -----------------------------
#     # SEARCH HANDLER
#     # -----------------------------
#     def _handle_search(self, text: str):
#         query = (
#             text.replace("search google for ", "")
#             .replace("search for ", "")
#             .replace("google ", "")
#             .replace("look up ", "")
#         )
#         if not query:
#             return False
#
#         encoded = urllib.parse.quote_plus(query)
#         self.page.goto(f"https://www.google.com/search?q={encoded}")
#         return True
#
#     # -----------------------------
#     # NEXT PAGE
#     # -----------------------------
#     def _handle_next_page(self):
#         url = self.page.url
#         if "google.com/search" in url:
#             try:
#                 self.page.click("a#pnnext")
#                 return True
#             except:
#                 return False
#         # fallback scroll
#         self.page.mouse.wheel(0, 1000)
#         return True
#
#     # -----------------------------
#     # SMART CLICK
#     # -----------------------------
#     def _handle_click(self, command):
#         words = command.split()
#         index = 0 if "first" in words else 1 if "second" in words else 2 if "third" in words else None
#         if index is None:
#             return False
#
#         url = self.page.url
#         # Google results
#         if "google.com/search" in url:
#             results = self.page.query_selector_all("h3")
#             if len(results) > index:
#                 results[index].click()
#                 return True
#         # GitHub repos
#         if "github.com" in url:
#             repos = self.page.query_selector_all("a.v-align-middle")
#             if len(repos) > index:
#                 repos[index].click()
#                 return True
#         # Generic links
#         links = self.page.query_selector_all("a")
#         if len(links) > index:
#             links[index].click()
#             return True
#
#         return False
#
#     # -----------------------------
#     # YOUTUBE PLAY
#     # -----------------------------
#     def _handle_youtube_play(self):
#         url = self.page.url
#         if "youtube.com/watch" in url:
#             self.page.keyboard.press("k")
#             return True
#         if "youtube.com/results" in url:
#             videos = self.page.query_selector_all("a#video-title")
#             if videos:
#                 videos[0].click()
#                 return True
#         return False
#
#








# from playwright.sync_api import sync_playwright
# import urllib.parse
#
#
# class BrowserController:
#     def __init__(self):
#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(headless=False)
#         self.context = self.browser.new_context()
#         self.page = self.context.new_page()
#
#     # -----------------------------
#     # Main Command Router
#     # -----------------------------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower().strip()
#
#         print(f"[BrowserController] Received: {spoken_text}")
#
#         # 🔎 SEARCH COMMANDS
#         if spoken_text.startswith(("search for ", "google ", "search google for ", "look up ")):
#             return self._handle_search(spoken_text)
#
#         # 🌍 NAVIGATION
#         if spoken_text in ["go back", "back"]:
#             self.page.go_back()
#             return True
#
#         if spoken_text in ["go forward", "forward"]:
#             self.page.go_forward()
#             return True
#
#         if spoken_text in ["refresh", "reload"]:
#             self.page.reload()
#             return True
#
#         if spoken_text in ["scroll down"]:
#             self.page.mouse.wheel(0, 800)
#             return True
#
#         if spoken_text in ["scroll up"]:
#             self.page.mouse.wheel(0, -800)
#             return True
#
#         if spoken_text in ["zoom in"]:
#             self.page.evaluate("document.body.style.zoom = '110%'")
#             return True
#
#         if spoken_text in ["zoom out"]:
#             self.page.evaluate("document.body.style.zoom = '90%'")
#             return True
#
#         if spoken_text in ["next page"]:
#             return self._handle_next_page()
#
#         # 🖱 SMART CLICK COMMANDS
#         if spoken_text.startswith("click"):
#             return self._handle_click(spoken_text)
#
#         if spoken_text in ["play video"]:
#             return self._handle_youtube_play()
#
#         return False
#
#     # -----------------------------
#     # SEARCH HANDLER
#     # -----------------------------
#     def _handle_search(self, text):
#         query = (
#             text.replace("search google for ", "")
#                 .replace("search for ", "")
#                 .replace("google ", "")
#                 .replace("look up ", "")
#         )
#
#         if not query:
#             return False
#
#         encoded = urllib.parse.quote_plus(query)
#         self.page.goto(f"https://www.google.com/search?q={encoded}")
#         return True
#
#     # -----------------------------
#     # NEXT PAGE (Google-aware)
#     # -----------------------------
#     def _handle_next_page(self):
#         url = self.page.url
#
#         if "google.com/search" in url:
#             try:
#                 self.page.click("a#pnnext")
#                 return True
#             except:
#                 return False
#
#         # fallback scroll
#         self.page.mouse.wheel(0, 1000)
#         return True
#
#     # -----------------------------
#     # SMART CLICK (Google + Generic)
#     # -----------------------------
#     def _handle_click(self, command):
#         words = command.split()
#
#         if "first" in words:
#             index = 0
#         elif "second" in words:
#             index = 1
#         elif "third" in words:
#             index = 2
#         else:
#             return False
#
#         url = self.page.url
#
#         # Google results
#         if "google.com/search" in url:
#             results = self.page.query_selector_all("h3")
#             if len(results) > index:
#                 results[index].click()
#                 return True
#
#         # GitHub repos
#         if "github.com" in url:
#             repos = self.page.query_selector_all("a.v-align-middle")
#             if len(repos) > index:
#                 repos[index].click()
#                 return True
#
#         # Generic links
#         links = self.page.query_selector_all("a")
#         if len(links) > index:
#             links[index].click()
#             return True
#
#         return False
#
#     # -----------------------------
#     # YOUTUBE PLAY HANDLER
#     # -----------------------------
#     def _handle_youtube_play(self):
#         url = self.page.url
#
#         if "youtube.com/watch" in url:
#             self.page.keyboard.press("k")  # YouTube play shortcut
#             return True
#
#         # If on search page, click first video
#         if "youtube.com/results" in url:
#             videos = self.page.query_selector_all("a#video-title")
#             if videos:
#                 videos[0].click()
#                 return True
#
#         return False








# modules/browser_controller.py
#
# import urllib.parse
# from playwright.sync_api import sync_playwright
#
#
# class BrowserController:
#     def __init__(self):
#         self.playwright = None
#         self.browser = None
#         self.context = None
#         self.page = None
#         self.started = False
#
#     # ---------- Startup ----------
#     def start(self):
#         if self.started:
#             return
#
#         self.playwright = sync_playwright().start()
#         self.browser = self.playwright.chromium.launch(
#             headless=False,
#             args=["--start-maximized"]
#         )
#         self.context = self.browser.new_context()
#         self.page = self.context.new_page()
#         self.started = True
#
#         print("[Browser] Playwright browser started.")
#
#     def ensure_started(self):
#         if not self.started:
#             self.start()
#
#     # ---------- Google Search ----------
#     def google_search(self, query: str):
#         self.ensure_started()
#         encoded = urllib.parse.quote_plus(query)
#         url = f"https://www.google.com/search?q={encoded}"
#         self.page.goto(url)
#         print(f"[Browser] Searching Google for: {query}")
#
#     # ---------- Navigation ----------
#     def go_back(self):
#         self.ensure_started()
#         self.page.go_back()
#         print("[Browser] Going back.")
#
#     def go_forward(self):
#         self.ensure_started()
#         self.page.go_forward()
#         print("[Browser] Going forward.")
#
#     def refresh(self):
#         self.ensure_started()
#         self.page.reload()
#         print("[Browser] Refreshing page.")
#
#     def next_page(self):
#         self.ensure_started()
#
#         # Google-specific next page
#         if "google" in self.page.url:
#             try:
#                 self.page.locator("#pnnext").click(timeout=3000)
#                 print("[Browser] Google next page.")
#                 return
#             except:
#                 pass
#
#         # Fallback: PageDown
#         self.page.keyboard.press("PageDown")
#         print("[Browser] Generic next page (PageDown).")
#
#     # ---------- Scrolling ----------
#     def scroll_down(self):
#         self.ensure_started()
#         self.page.mouse.wheel(0, 1200)
#         print("[Browser] Scrolling down.")
#
#     def scroll_up(self):
#         self.ensure_started()
#         self.page.mouse.wheel(0, -1200)
#         print("[Browser] Scrolling up.")
#
#     # ---------- Zoom ----------
#     def zoom_in(self):
#         self.ensure_started()
#         self.page.keyboard.down("Control")
#         self.page.keyboard.press("+")
#         self.page.keyboard.up("Control")
#         print("[Browser] Zooming in.")
#
#     def zoom_out(self):
#         self.ensure_started()
#         self.page.keyboard.down("Control")
#         self.page.keyboard.press("-")
#         self.page.keyboard.up("Control")
#         print("[Browser] Zooming out.")
#
#     # ---------- Tabs ----------
#     def new_tab(self):
#         self.ensure_started()
#         self.page = self.context.new_page()
#         print("[Browser] Opened new tab.")
#
#     def close_tab(self):
#         self.ensure_started()
#         self.page.close()
#         if self.context.pages:
#             self.page = self.context.pages[-1]
#         print("[Browser] Closed current tab.")
#
#     # ---------- Generic Command Router ----------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower().strip()
#
#         # Google search triggers
#         if spoken_text.startswith("search google for "):
#             query = spoken_text.replace("search google for ", "", 1)
#             self.google_search(query)
#             return True
#
#         if spoken_text.startswith("google "):
#             query = spoken_text.replace("google ", "", 1)
#             self.google_search(query)
#             return True
#
#         # Navigation
#         if spoken_text in ["back", "go back"]:
#             self.go_back()
#             return True
#
#         if spoken_text in ["forward", "go forward"]:
#             self.go_forward()
#             return True
#
#         if spoken_text in ["refresh", "reload"]:
#             self.refresh()
#             return True
#
#         if spoken_text in ["next page"]:
#             self.next_page()
#             return True
#
#         # Scroll
#         if spoken_text in ["scroll down"]:
#             self.scroll_down()
#             return True
#
#         if spoken_text in ["scroll up"]:
#             self.scroll_up()
#             return True
#
#         # Zoom
#         if spoken_text in ["zoom in"]:
#             self.zoom_in()
#             return True
#
#         if spoken_text in ["zoom out"]:
#             self.zoom_out()
#             return True
#
#         # Tabs
#         if spoken_text in ["new tab", "open new tab"]:
#             self.new_tab()
#             return True
#
#         if spoken_text in ["close tab"]:
#             self.close_tab()
#             return True
#
#         return False



# General Voice commands for play write

# import random
# import time
# from playwright.sync_api import sync_playwright
# from playwright_stealth import Stealth
#
#
# def human_delay(min_s=0.4, max_s=1.2):
#     time.sleep(random.uniform(min_s, max_s))
#
#
# def add_esp32_to_cart():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             headless=False,
#             args=[
#                 "--disable-blink-features=AutomationControlled",
#                 "--start-maximized"
#             ]
#         )
#
#         context = browser.new_context(
#             viewport={"width": 1366, "height": 768},
#             user_agent=(
#                 "Mozilla/5.0 (X11; Linux x86_64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/120.0.0.0 Safari/537.36"
#             ),
#             locale="en-US",
#         )
#
#         page = context.new_page()
#
#         # Apply stealth properly (v2 API)
#         stealth = Stealth()
#         stealth.apply_stealth_sync(page)
#
#         # Go to Amazon
#         page.goto("https://www.amazon.com", wait_until="domcontentloaded")
#         human_delay()
#
#         # Accept cookies if prompted
#         try:
#             page.locator("input[name='accept']").click(timeout=2000)
#         except:
#             pass
#
#         # Search for ESP32
#         search_box = page.locator("#twotabsearchtextbox")
#         search_box.click()
#         human_delay()
#         search_box.type("ESP32", delay=100)
#         human_delay()
#         page.click("#nav-search-submit-button")
#
#         page.wait_for_selector("div[data-component-type='s-search-result']")
#         human_delay(1, 2)
#
#         # Click first result safely
#         first_result = page.locator(
#             "div[data-component-type='s-search-result'] h2 a"
#         ).first
#
#         first_result.click()
#         page.wait_for_load_state("domcontentloaded")
#         human_delay(1, 2)
#
#         # Try to add to cart
#         try:
#             page.locator("#add-to-cart-button").click(timeout=5000)
#             print("✅ ESP32 added to cart!")
#         except Exception as e:
#             print("❌ Failed to add to cart:", e)
#
#         human_delay(3, 5)
#         browser.close()
#
#
# if __name__ == "__main__":
#     add_esp32_to_cart()
