import os
from queue import Queue
from modules.browser_controller import BrowserController
from modules.window_controller import WindowController


class AppLauncher:
    def __init__(self, window_controller: WindowController):
        self.current_app = None
        self.window_controller = window_controller

        # Browser queue for async commands
        self.browser_queue: Queue = Queue()
        self.browser_controller = BrowserController(self.browser_queue)

        # Browser triggers
        self.browser_triggers = [
            "search google for", "google", "look up", "search for"
        ]

        # Native apps and aliases
        self.apps = {
            "pycharm": {
                "path": "/opt/pycharm/bin/pycharm.sh",
                "shortcut_key": "pycharm",
                "aliases": [
                    "pycharm", "charm", "idea", "jetbrains",
                    "open pycharm", "launch pycharm", "python"
                ],
            },
            "vscode": {
                "path": "/usr/bin/code",
                "shortcut_key": "code",
                "aliases": [
                    "vscode", "visual studio code", "code editor",
                    "launch vscode", "code"
                ],
            },
            "browser": {
                "path": "/usr/bin/firefox",
                "shortcut_key": "firefox",
                "aliases": [
                    "firefox", "browser", "open browser",
                    "launch firefox", "bowser"
                ],
            },
            "terminal": {
                "path": "/usr/bin/cosmic-term",
                "shortcut_key": "cosmic-term",
                "aliases": [
                    "terminal", "shell", "open terminal", "launch terminal"
                ],
            },
        }

    # ---------- Launch native app ----------
    def open_app(self, spoken_text: str) -> str | bool:
        spoken_text = spoken_text.lower()
        for app_name, info in self.apps.items():
            for alias in info["aliases"]:
                if alias in spoken_text:
                    print(f"[Launcher] Launching {app_name}...")
                    os.system(f'"{info["path"]}" &')
                    self.current_app = app_name
                    self.window_controller.update_active_window(app_name)
                    return info.get("shortcut_key", app_name.lower())
        return False

    # ---------- Handle all commands ----------
    def handle_command(self, spoken_text: str) -> bool:
        spoken_text = spoken_text.lower().strip()

        # 1️⃣ Browser commands
        if any(trigger in spoken_text for trigger in self.browser_triggers):
            self.browser_controller.handle_command(spoken_text)
            self.current_app = "browser"
            return True

        # 2️⃣ Launch native app
        if self.open_app(spoken_text):
            return True

        # 3️⃣ Active app hotkeys
        if self.current_app and self.current_app != "browser":
            if self.window_controller.send_command(spoken_text):
                return True

        # 4️⃣ Not recognized
        return False

    # ---------- Getter ----------
    def get_current_app(self):
        return self.current_app







# # modules/app_launcher.py
# import os
# from modules.browser_controller import BrowserController
# from modules.window_controller import WindowController
# import queue
#
# class AppLauncher:
#     def __init__(self, window_controller=None):
#         # Thread-safe queue for browser commands
#         self.browser_queue = queue.Queue()
#         self.browser_controller = BrowserController(browser_queue=self.browser_queue)
#
#         self.window_controller = WindowController(app_launcher=self)
#         self.current_app = None
#
#         self.browser_triggers = [
#             "search google for",
#             "google",
#             "look up",
#             "search for"
#         ]
#
#         self.apps = {
#             "pycharm": {
#                 "path": "/opt/pycharm/bin/pycharm.sh",
#                 "shortcut_key": "pycharm",
#                 "aliases": ["pycharm", "charm", "idea", "jetbrains", "open pycharm", "launch pycharm", "python"],
#             },
#             "vscode": {
#                 "path": "/usr/bin/code",
#                 "shortcut_key": "code",
#                 "aliases": ["vscode", "visual studio code", "code editor", "launch vscode", "code"],
#             },
#             "browser": {
#                 "path": "/usr/bin/firefox",
#                 "shortcut_key": "firefox",
#                 "aliases": ["firefox", "browser", "open browser", "launch firefox", "bowser"],
#             },
#             "terminal": {
#                 "path": "/usr/bin/cosmic-term",
#                 "shortcut_key": "cosmic-term",
#                 "aliases": ["terminal", "shell", "open terminal", "launch terminal"],
#             },
#         }
#
#     # ---------- Open Native App ----------
#     def open_app(self, spoken_text: str) -> str | bool:
#         spoken_text = spoken_text.lower()
#         for app_name, app_info in self.apps.items():
#             for alias in app_info["aliases"]:
#                 if alias in spoken_text:
#                     print(f"[Launcher] Launching {app_name}...")
#                     os.system(f'"{app_info["path"]}" &')
#                     self.current_app = app_name
#                     self.window_controller.update_active_window(app_name)
#                     return app_info.get("shortcut_key", app_name.lower())
#         return False
#
#     # ---------- Handle Commands ----------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower().strip()
#
#         # Browser first
#         if any(trigger in spoken_text for trigger in self.browser_triggers):
#             print(f"[Launcher] Queueing command for browser: {spoken_text}")
#             self.browser_controller.queue_command(spoken_text)
#             self.current_app = "browser"
#             return True
#
#         # Native apps
#         if self.open_app(spoken_text):
#             return True
#
#         # Active app hotkeys
#         if self.current_app and self.current_app != "browser":
#             if self.window_controller.send_command(spoken_text):
#                 return True
#
#         print(f"[Launcher] Command not recognized: {spoken_text}")
#         return False
#
#     def get_current_app(self):
#         return self.current_app







# import os
# from modules.browser_controller import BrowserController
# from modules.window_controller import WindowController
#
#
# class AppLauncher:
#     def __init__(self, window_controller=None, browser_queue=None):
#         # Persistent BrowserController for Playwright or other browser actions
#         self.browser_controller = BrowserController(browser_queue=browser_queue)
#
#         # WindowController for native apps
#         self.window_controller = WindowController(app_launcher=self)
#
#         # Track the current active app
#         self.current_app = None
#
#         # Commands that should go to the browser
#         self.browser_triggers = [
#             "search google for",
#             "google",
#             "look up",
#             "search for"
#         ]
#
#         # Define native apps with aliases
#         self.apps = {
#             "pycharm": {
#                 "path": "/opt/pycharm/bin/pycharm.sh",
#                 "shortcut_key": "pycharm",
#                 "aliases": [
#                     "pycharm", "charm", "idea", "jetbrains",
#                     "open pycharm", "launch pycharm", "python"
#                 ],
#             },
#             "vscode": {
#                 "path": "/usr/bin/code",
#                 "shortcut_key": "code",
#                 "aliases": [
#                     "vscode", "visual studio code", "code editor",
#                     "launch vscode", "code"
#                 ],
#             },
#             "browser": {
#                 "path": "/usr/bin/firefox",
#                 "shortcut_key": "firefox",
#                 "aliases": [
#                     "firefox", "browser", "open browser",
#                     "launch firefox", "bowser"
#                 ],
#             },
#             "terminal": {
#                 "path": "/usr/bin/cosmic-term",
#                 "shortcut_key": "cosmic-term",
#                 "aliases": [
#                     "terminal", "shell", "open terminal", "launch terminal",
#                 ],
#             },
#         }
#
#     # ---------- Open Native App ----------
#     def open_app(self, spoken_text: str) -> str | bool:
#         spoken_text = spoken_text.lower()
#
#         for app_name, app_info in self.apps.items():
#             for alias in app_info["aliases"]:
#                 if alias in spoken_text:
#                     print(f"[Launcher] Launching {app_name}...")
#                     os.system(f'"{app_info["path"]}" &')
#                     self.current_app = app_name
#                     # Update WindowController active window
#                     self.window_controller.update_active_window(app_name)
#                     return app_info.get("shortcut_key", app_name.lower())
#         return False
#
#     # ---------- Main Command Router ----------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower().strip()
#
#         # 1️⃣ Browser commands first (persistent controller)
#         if any(trigger in spoken_text for trigger in self.browser_triggers):
#             print(f"[Launcher] Sending command to BrowserController: {spoken_text}")
#             self.browser_controller.queue_command(spoken_text)
#             self.current_app = "browser"
#             return True
#
#         # 2️⃣ Native app launch
#         if self.open_app(spoken_text):
#             return True
#
#         # 3️⃣ Active app hotkeys via WindowController
#         if self.current_app and self.current_app != "browser":
#             if self.window_controller.send_command(spoken_text):
#                 return True
#
#         # 4️⃣ Command not recognized
#         print(f"[Launcher] Command not recognized: {spoken_text}")
#         return False
#
#     # ---------- Getter ----------
#     def get_current_app(self):
#         return self.current_app








# import os
# from modules.browser_controller import BrowserController
# from modules.window_controller import WindowController
#
#
# class AppLauncher:
#     def __init__(self, window_controller):
#         # Persistent browser
#         self.browser_controller = BrowserController()
#         # WindowController for native apps
#         self.window_controller = WindowController(app_launcher=self)
#         # Track current app
#         self.current_app = None
#         self.browser_triggers = [
#             "search google for",
#             "google",
#             "look up",
#             "search for"
#         ]
#
#         # Define apps and aliases
#         self.apps = {
#             "pycharm": {
#                 "path": "/opt/pycharm/bin/pycharm.sh",
#                 "shortcut_key": "pycharm",
#                 "aliases": [
#                     "pycharm", "charm", "idea", "jetbrains",
#                     "open pycharm", "launch pycharm", "python"
#                 ],
#             },
#             "vscode": {
#                 "path": "/usr/bin/code",
#                 "shortcut_key": "code",
#                 "aliases": [
#                     "vscode", "visual studio code", "code editor",
#                     "launch vscode", "code"
#                 ],
#             },
#             "browser": {
#                 "path": "/usr/bin/firefox",
#                 "shortcut_key": "firefox",
#                 "aliases": [
#                     "firefox", "browser", "open browser",
#                     "launch firefox", "bowser"
#                 ],
#             },
#             "terminal": {
#                 "path": "/usr/bin/cosmic-term",
#                 "shortcut_key": "cosmic-term",
#                 "aliases": [
#                     "terminal", "shell", "open terminal", "launch terminal",
#                 ],
#             },
#         }
#
#     # ---------- Open Native App ----------
#     def open_app(self, spoken_text: str) -> str | bool:
#         spoken_text = spoken_text.lower()
#
#         for app_name, app_info in self.apps.items():
#             for alias in app_info["aliases"]:
#                 if alias in spoken_text:
#                     print(f"[Launcher] Launching {app_name}...")
#                     os.system(f'"{app_info["path"]}" &')
#                     self.current_app = app_name
#                     # Update WindowController active window
#                     self.window_controller.update_active_window(app_name)
#                     return app_info.get("shortcut_key", app_name.lower())
#         return False
#
#     # ---------- Main Command Router ----------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower().strip()
#
#         # 1️⃣ Browser commands first
#         if self.browser_controller.handle_command(spoken_text):
#             self.current_app = "browser"
#             return True
#
#         # 2️⃣ Native app launch
#         if self.open_app(spoken_text):
#             return True
#
#         # 3️⃣ Active app hotkeys via WindowController
#         if self.current_app and self.current_app != "browser":
#             if self.window_controller.send_command(spoken_text):
#                 return True
#
#         # 4️⃣ Command not recognized
#         print(f"[Launcher] Command not recognized: {spoken_text}")
#         return False
#
#     # ---------- Getter ----------
#     def get_current_app(self):
#         return self.current_app
#
#









# import os
# from modules.browser_controller import BrowserController
#
# class AppLauncher:
#     def __init__(self, window_controller=None):
#         # Tracks the last launched app for command routing
#         self.window_controller = window_controller
#         self.browser_controller = BrowserController()
#         self.current_app = None
#
#         # Define apps and aliases
#         self.apps = {
#             "pycharm": {
#                 "path": "/opt/pycharm/bin/pycharm.sh",
#                 "shortcut_key": "pycharm",
#                 "aliases": [
#                     "pycharm", "charm", "idea", "jetbrains",
#                     "open pycharm", "launch pycharm", "python"
#                 ],
#             },
#             "vscode": {
#                 "path": "/usr/bin/code",
#                 "shortcut_key": "code",
#                 "aliases": [
#                     "vscode", "visual studio code", "code editor",
#                     "launch vscode", "code"
#                 ],
#             },
#             "browser": {
#                 "path": "/usr/bin/firefox",
#                 "shortcut_key": "firefox",
#                 "aliases": [
#                     "firefox", "browser", "open browser",
#                     "launch firefox", "bowser"
#                 ],
#             },
#             "terminal": {
#                 "path": "/usr/bin/cosmic-term",
#                 "shortcut_key": "cosmic-term",
#                 "aliases": [
#                     "terminal", "shell", "open terminal", "launch terminal",
#                 ],
#             },
#         }
#
#     # ---------- Open Native App ----------
#     def open_app(self, spoken_text: str) -> str | bool:
#         """
#         Attempt to open a native app based on spoken text.
#         Returns the app's shortcut_key if launched, otherwise False.
#         """
#         spoken_text = spoken_text.lower()
#
#         for app_name, app_info in self.apps.items():
#             for alias in app_info["aliases"]:
#                 if alias in spoken_text:
#                     print(f"[Launcher] Launching {app_name}...")
#                     os.system(f'"{app_info["path"]}" &')
#
#                     # Track current app
#                     self.current_app = app_name
#
#                     return app_info.get("shortcut_key", app_name.lower())
#
#         return False
#
#     # ---------- Main Command Router ----------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower().strip()
#
#         # 1️⃣ Priority: Browser commands
#         if self.browser_controller.handle_command(spoken_text):
#             self.current_app = "browser"
#             return True
#
#         # 2️⃣ Priority: Launch native apps
#         if self.open_app(spoken_text):
#             return True
#
#         # 3️⃣ Unrecognized
#         print(f"[Launcher] Command not recognized: {spoken_text}")
#         return False
#
#     # ---------- Getter for Last Launched App ----------
#     def get_current_app(self):
#         return self.current_app





# import os
# import subprocess
# import urllib.parse
# from modules.browser_controller import BrowserController
#
#
# class AppLauncher:
#     def __init__(self, window_controller=None):
#         # Tracks the last launched app for command routing
#         self.window_controller = window_controller
#         self.browser_controller = BrowserController()
#         self.current_app = None
#
#         # Define apps and aliases
#         self.apps = {
#             "pycharm": {
#                 "path": "/opt/pycharm/bin/pycharm.sh",
#                 "shortcut_key": "pycharm",
#                 "aliases": [
#                     "pycharm",
#                     "charm",
#                     "idea",
#                     "jetbrains",
#                     "open pycharm",
#                     "launch pycharm",
#                     "python"
#                 ],
#             },
#             "vscode": {
#                 "path": "/usr/bin/code",
#                 "shortcut_key": "code",
#                 "aliases": [
#                     "vscode",
#                     "visual studio code",
#                     "code editor",
#                     "launch vscode",
#                     "code"
#                 ],
#             },
#             "browser": {
#                 "path": "/usr/bin/firefox",
#                 "shortcut_key": "firefox",
#                 "aliases": [
#                     "firefox",
#                     "browser",
#                     "open browser",
#                     "launch firefox",
#                     "bowser"
#                 ],
#             },
#             "terminal": {
#                 "path": "/usr/bin/cosmic-term",
#                 "shortcut_key": "cosmic-term",
#                 "aliases": [
#                     "terminal",
#                     "shell",
#                     "open terminal",
#                     "launch terminal",
#                 ],
#             },
#         }
#
#         self.google_triggers = [
#             "search google for",
#             "google",
#             "look up",
#             "search for"
#         ]
#
#     # ---------- Google Search ----------
#     def google_search(self, spoken_text: str) -> bool:
#         words = spoken_text.split()
#         if not words:
#             return False
#
#         if words[0] == "google":
#             query = " ".join(words[1:])
#         elif spoken_text.startswith("search for "):
#             query = spoken_text.replace("search for ", "", 1)
#         elif spoken_text.startswith("look up "):
#             query = spoken_text.replace("look up ", "", 1)
#         else:
#             return False
#
#         if not query:
#             print("[Launcher] No search query detected.")
#             return False
#
#         print(f"[Launcher] Google searching: {query}")
#         encoded_query = urllib.parse.quote_plus(query)
#
#         subprocess.Popen([
#             "xdg-open",
#             f"https://www.google.com/search?q={encoded_query}"
#         ])
#         return True
#
#     # ---------- Open App ----------
#     def open_app(self, spoken_text: str) -> str | bool:
#         """
#         Attempt to open an app based on spoken text.
#         Returns the app's shortcut_key if launched, otherwise False.
#         """
#         spoken_text = spoken_text.lower()
#
#         for app_name, app_info in self.apps.items():
#             for alias in app_info["aliases"]:
#                 if alias in spoken_text:
#                     print(f"[Launcher] Launching {app_name}...")
#                     os.system(f'"{app_info["path"]}" &')
#
#                     # Track current app
#                     self.current_app = app_name
#
#                     # Return the shortcut_key for WindowController routing
#                     return app_info.get("shortcut_key", app_name.lower())
#
#         return False
#
#     # ---------- Main Router ----------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower()
#
#         # 1️⃣ Browser commands first (persistent session)
#         if self.browser_controller.handle_command(spoken_text):
#             self.current_app = "browser"
#             return True
#
#         # 2️⃣ Launch native apps
#         if self.open_app(spoken_text):
#             return True
#
#         print(f"[Launcher] Command not recognized: {spoken_text}")
#         return False
#
#     # def handle_command(self, spoken_text: str) -> bool:
#     #     spoken_text = spoken_text.lower()
#     #
#     #     # 1️⃣ Priority: Google Search
#     #     if self.google_search(spoken_text):
#     #         return True
#     #
#     #     # 2️⃣ Priority: Launch App
#     #     if self.open_app(spoken_text):
#     #         return True
#     #
#     #     # Unrecognized
#     #     print(f"[Launcher] Command not recognized: {spoken_text}")
#     #     return False
#
#     # ---------- Getter for Last Launched App ----------
#     def get_current_app(self):
#         return self.current_app



    # X11 version
    # def open_app(self, spoken_text: str) -> bool:
    #     spoken_text = spoken_text.lower()
    #
    #     for app_name, app_info in self.apps.items():
    #         for alias in app_info["aliases"]:
    #             if alias in spoken_text:
    #                 print(f"[Launcher] Launching {app_name}...")
    #                 os.system(f'"{app_info["path"]}" &')
    #
    #                 self.current_app = app_name
    #
    #                 # 🔥 Notify WindowController with correct shortcut key
    #                 if self.window_controller:
    #                     shortcut_key = app_info.get("shortcut_key", app_name)
    #                     self.window_controller.update_active_window(shortcut_key)
    #
    #                 return True
    #
    #     return False

# import os
# import subprocess
# import urllib.parse
#
#
# class AppLauncher:
#     def __init__(self):
#         self.current_app = None
#         self.apps = {
#             "pycharm": {
#                 "path": "/opt/pycharm/bin/pycharm.sh",
#                 "aliases": [
#                     "pycharm",
#                     "charm",
#                     "idea",
#                     "jetbrains",
#                     "open pycharm",
#                     "launch pycharm",
#                     "python"
#                 ],
#             },
#             "vscode": {
#                 "path": "/usr/bin/code",
#                 "aliases": [
#                     "vscode",
#                     "visual studio code",
#                     "code editor",
#                     "launch vscode",
#                     "code"
#                 ],
#             },
#             "browser": {
#                 "path": "/usr/bin/firefox",
#                 "aliases": [
#                     "firefox",
#                     "browser",
#                     "open browser",
#                     "launch firefox",
#                     "bowser"
#                 ],
#             },
#             "terminal": {
#                 "path": "/usr/bin/cosmic-term",
#                 "aliases": [
#                     "terminal",
#                     "shell",
#                     "open terminal",
#                     "launch terminal",
#                 ],
#             },
#         }
#
#         self.google_triggers = [
#             "search google for",
#             "google",
#             "look up",
#             "search for"
#         ]
#
#     # ---------- Google Search ----------
#     def google_search(self, spoken_text: str) -> bool:
#         words = spoken_text.split()
#
#         if not words:
#             return False
#
#         if words[0] == "google":
#             query = " ".join(words[1:])
#         elif spoken_text.startswith("search for "):
#             query = spoken_text.replace("search for ", "", 1)
#         elif spoken_text.startswith("look up "):
#             query = spoken_text.replace("look up ", "", 1)
#         else:
#             return False
#
#         if not query:
#             print("[Launcher] No search query detected.")
#             return False
#
#         print(f"[Launcher] Google searching: {query}")
#         encoded_query = urllib.parse.quote_plus(query)
#
#         subprocess.Popen([
#             "xdg-open",
#             f"https://www.google.com/search?q={encoded_query}"
#         ])
#         return True
#
#     # ---------- Open App ----------
#     def open_app(self, spoken_text: str) -> str:
#         for app_name, app_info in self.apps.items():
#             for alias in app_info["aliases"]:
#                 if alias in spoken_text:
#                     print(f"[Launcher] Launching {app_name}...")
#                     os.system(f'"{app_info["path"]}" &')
#                     return f"Opening {app_name}"
#
#         return False
#
#     # ---------- Main Router ----------
#     def handle_command(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower()
#
#         # Priority 1: Google Search
#         if self.google_search(spoken_text):
#             return True
#
#         # Priority 2: App Launch
#         if self.open_app(spoken_text):
#             return True
#
#         print(f"[Launcher] Command not recognized: {spoken_text}")
#         return False




# import subprocess
# import shlex
# import os
#
#
# class AppLauncher:
#     def __init__(self):
#         self.apps = {
#             "pycharm": {
#                 "path": "/opt/pycharm/bin/pycharm.sh",
#                 "aliases": [
#                     "pycharm",
#                     "charm",
#                     "idea",
#                     "jetbrains",
#                     "open pycharm",
#                     "launch pycharm",
#                     "python"
#                 ],
#             },
#             "vscode": {
#                 "path": "/usr/bin/code",
#                 "aliases": [
#                     "vscode",
#                     "visual studio code",
#                     "code editor",
#                     "launch vscode",
#                     "code"
#                 ],
#             },
#             "browser": {
#                 "path": "/usr/bin/firefox",
#                 "aliases": [
#                     "firefox",
#                     "browser",
#                     "open browser",
#                     "launch firefox",
#                     "Bowser"
#                 ],
#             },
#             "terminal": {
#                 "path": "/usr/bin/cosmic-term",
#                 "aliases": [
#                     "terminal",
#                     "shell",
#                     "open terminal",
#                     "launch terminal",
#                 ],
#             },
#         }
#
#     def open_app(self, spoken_text: str) -> bool:
#         spoken_text = spoken_text.lower()
#
#         for app_name, app_info in self.apps.items():
#             for alias in app_info["aliases"]:
#                 if alias in spoken_text:
#                     print(f"[Launcher] Launching {app_name}...")
#                     os.system(f'"{app_info["path"]}" &')
#
#                     google_triggers = ["search google for", "google", "look up", "search for"]
#                     for trigger in google_triggers:
#                         if trigger in spoken_text:
#                             print(f'Google search for {spoken_text}')
#                             # Extract query after the trigger phrase
#                             query = spoken_text.split(trigger, 1)[1].strip()
#                             if query:
#                                 # speak(f"Searching Google for {query}")
#                                 os.system(f"xdg-open 'https://www.google.com/search?q={query.replace(' ', '+')}'")
#                                 return True
#                     return True
#
#         print(f"[Launcher] App not recognized in: {spoken_text}")
#         return False

    # def google_search(self, command):
    #     # Might be redundant
    #     # Define Google search triggers
    #     google_triggers = ["search google for", "google", "look up", "search for"]
    #     for trigger in google_triggers:
    #         if trigger in command:
    #             # Extract query after the trigger phrase
    #             query = command.split(trigger, 1)[1].strip()
    #             if query:
    #                 # speak(f"Searching Google for {query}")
    #                 os.system(f"xdg-open 'https://www.google.com/search?q={query.replace(' ', '+')}'")
    #                 return True
    #     return False




    # def open_app(self, spoken_name):
    #     spoken_name = spoken_name.lower()
    #     for key, path in self.apps.items():
    #         if key in spoken_name:
    #             print(f"[Launcher] Opening {key}...")
    #             try:
    #                 subprocess.Popen(shlex.split(path))
    #             except FileNotFoundError:
    #                 print(f"[Launcher] Executable not found: {path}")
    #             return True
    #     return False













# import subprocess
# import shlex
#
#
# class AppLauncher:
#     def __init__(self):
#         self.apps = {
#             "pycharm": "/opt/pycharm/bin/pycharm.sh",
#             "vscode": "/usr/bin/code",
#             "browser": "/usr/bin/firefox",
#         }
#
#     def open_app(self, spoken_name):
#         spoken_name = spoken_name.lower()
#         for key, path in self.apps.items():
#             if key in spoken_name:
#                 print(f"[Launcher] Opening {key}...")
#                 try:
#                     subprocess.Popen(shlex.split(path))
#                 except FileNotFoundError:
#                     print(f"[Launcher] Executable not found: {path}")
#                 return True
#         return False
























# import subprocess
# import shlex
#
#
# class AppLauncher:
#     def __init__(self):
#         self.apps = {
#             "pycharm": "/opt/pycharm/bin/pycharm.sh",
#             "vscode": "/opt/pycharm/bin/code",
#             "browser": "/usr/bin/firefox",
#         }
#
#     def open_app(self, spoken_name):
#         spoken_name = spoken_name.lower()
#         for key, path in self.apps.items():
#             if key in spoken_name:
#                 print(f"[Launcher] Opening {key}...")
#                 try:
#                     subprocess.Popen(shlex.split(path))
#                 except FileNotFoundError:
#                     print(f"[Launcher] Executable not found: {path}")
#                 return True
#         return False

































# class AppLauncher:
#     def __init__(self):
#         self.apps = {
#             "pycharm": "/opt/pycharm/bin/pycharm.sh",
#             "vscode": "/opt/pycharm/bin/code",
#             "browser": "/usr/bin/firefox",
#         }
#
#     def open_app(self, spoken_name):
#         spoken_name = spoken_name.lower()
#         for key, path in self.apps.items():
#             if key in spoken_name:
#                 print(f"[Launcher] Opening {key}...")
#                 try:
#                     subprocess.Popen(shlex.split(path))
#                 except FileNotFoundError:
#                     print(f"[Launcher] Executable not found: {path}")
#                 return True
#         return False




















# class AppLauncher:
#     def __init__(self):
#         # Map spoken names to executable paths
#         self.apps = {
#             "pycharm": "/opt/pycharm/bin/pycharm.sh",
#             "vscode": "/opt/pycharm/bin/code",  # adjust if different
#             "browser": "/usr/bin/firefox",
#         }
#
#     def open_app(self, spoken_name):
#         spoken_name = spoken_name.lower()
#         for key, path in self.apps.items():
#             if key in spoken_name:
#                 print(f"[Launcher] Opening {key}...")
#                 try:
#                     subprocess.Popen(shlex.split(path))
#                 except FileNotFoundError:
#                     print(f"[Launcher] Executable not found: {path}")
#                 return
#         print(f"[Launcher] App not recognized: {spoken_name}")



    # def open_app(self, spoken_name):
    #     # Normalize name
    #     app_name = spoken_name.lower().replace("open ", "").strip()
    #
    #     if app_name in self.apps:
    #         path = self.apps[app_name]
    #         print(f"[Launcher] Opening {app_name}...")
    #         try:
    #             # Use shlex.split in case path has spaces
    #             subprocess.Popen(shlex.split(path))
    #         except FileNotFoundError:
    #             print(f"[Launcher] Executable not found: {path}")
    #     else:
    #         print(f"[Launcher] App not recognized: {app_name}")
