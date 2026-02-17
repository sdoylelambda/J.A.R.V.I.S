import subprocess
import re


# Generic Window Controller
# Code for Wayland (x11 is below commented out)
class WindowController:
    """App-aware window controller, Wayland-compatible via ydotool."""

    # Map human-readable keys to Linux input keycodes for ydotool
    KEY_MAP = {
        "ctrl": "29",
        "shift": "42",
        "alt": "56",
        "super": "125",
        "tab": "15",
        "r": "19",
        "t": "20",
        "n": "57",
        "w": "17",
        "l": "38",
        "c": "46",
        "v": "47",
        "x": "45",
        "a": "30",
        "f5": "63",
        # Add more keys as needed
    }

    def __init__(self, app_launcher=None):
        self.launcher = app_launcher
        self.last_launched_app = None

        # App-specific shortcuts
        self.app_shortcuts = {
            "code": {  # VSCode
                "save": ["ctrl", "s"],
                "run": ["ctrl", "f5"],
                "new file": ["ctrl", "n"],
                "close tab": ["ctrl", "w"],
            },
            "firefox": {
                "new tab": ["ctrl", "t"],
                "close tab": ["ctrl", "w"],
                "refresh": ["ctrl", "r"],
                "reload": ["ctrl", "r"],
            },
            "terminal": {
                "new tab": ["ctrl", "shift", "t"],
                "clear": ["ctrl", "l"],
                "copy": ["ctrl", "shift", "c"],
                "paste": ["ctrl", "shift", "v"],
            }
        }

        # Generic fallback shortcuts
        self.generic_shortcuts = {
            "copy": ["ctrl", "c"],
            "paste": ["ctrl", "v"],
            "cut": ["ctrl", "x"],
            "select all": ["ctrl", "a"],
        }

    # ------------------------
    # Core Execution using ydotool
    # ------------------------
    def execute_hotkey(self, keys):
        """
        Convert key names to ydotool keycodes and send via ydotool.
        """
        print(f"[WindowController] Executing hotkey via ydotool: {keys}")

        sequence = []

        # Press down keys in order
        for key in keys:
            code = self.KEY_MAP.get(key.lower())
            if code:
                sequence.append(f"{code}:1")

        # Release keys in reverse order
        for key in reversed(keys):
            code = self.KEY_MAP.get(key.lower())
            if code:
                sequence.append(f"{code}:0")

        if sequence:
            try:
                subprocess.run(["ydotool", "key", *sequence], check=True)
            except Exception as e:
                print(f"[WindowController] Failed to execute hotkey: {e}")

    # ------------------------
    # Update last launched app
    # ------------------------
    def update_active_window(self, app_name: str):
        self.last_launched_app = app_name.lower()

    # ------------------------
    # Smart Command Router
    # ------------------------
    def send_command(self, command: str):
        command = command.lower().strip()
        command = re.sub(r"[^\w\s]", "", command)

        active_app = self.last_launched_app
        print(f"[WindowController] Active app: {active_app}")
        print(f"[WindowController] Heard command: {command}")

        # -------- App-Specific Commands --------
        if active_app and active_app in self.app_shortcuts:
            if self._match_and_execute(command, self.app_shortcuts[active_app]):
                return True

        # -------- Browser fallback --------
        browser_defaults = {
            "new tab": ["ctrl", "t"],
            "refresh": ["ctrl", "r"],
            "reload": ["ctrl", "r"],
            "close tab": ["ctrl", "w"],
        }

        if self._match_and_execute(command, browser_defaults):
            return True

        # -------- Generic fallback --------
        if self._match_and_execute(command, self.generic_shortcuts):
            return True

        return False

    # ------------------------
    # Matching Logic
    # ------------------------
    def _match_and_execute(self, command, shortcut_map):
        for phrase, keys in shortcut_map.items():
            if phrase in command:
                self.execute_hotkey(keys)
                return True
        return False







# Code for x11
# import pyautogui
# import re
#
#
# class WindowController:
#     """App-aware window controller, Wayland-compatible."""
#
#     def __init__(self, app_launcher=None):
#         self.launcher = app_launcher
#         self.last_launched_app = None
#
#         # App-specific shortcuts
#         self.app_shortcuts = {
#             "code": {  # VSCode
#                 "save": ["ctrl", "s"],
#                 "run": ["ctrl", "f5"],
#                 "new file": ["ctrl", "n"],
#                 "close tab": ["ctrl", "w"],
#             },
#             "firefox": {
#                 "new tab": ["ctrl", "t"],
#                 "close tab": ["ctrl", "w"],
#                 "refresh": ["ctrl", "r"],
#                 "reload": ["ctrl", "r"],
#             },
#             "terminal": {
#                 "new tab": ["ctrl", "shift", "t"],
#                 "clear": ["ctrl", "l"],
#                 "copy": ["ctrl", "shift", "c"],
#                 "paste": ["ctrl", "shift", "v"],
#             }
#         }
#
#         # Generic fallback shortcuts
#         self.generic_shortcuts = {
#             "copy": ["ctrl", "c"],
#             "paste": ["ctrl", "v"],
#             "cut": ["ctrl", "x"],
#             "select all": ["ctrl", "a"],
#         }
#
#     # ------------------------
#     # Active Window Detection
#     # ------------------------
#     # def get_active_window_name(self):    Does not work on Wayland - Works on X11
#     #     """
#     #     Detect currently focused window on Wayland using ydotool.
#     #     Fallback: last launched app.
#     #     """
#     #     try:
#     #         # Use ydotool to get focused window title (Wayland)
#     #         window_name = subprocess.check_output(
#     #             ["ydotool", "getwindowfocus", "getwindowname"],
#     #             stderr=subprocess.DEVNULL
#     #         ).strip().decode().lower()
#     #         return window_name
#     #     except Exception:
#     #         # If fails, fallback to last launched app
#     #         if self.last_launched_app:
#     #             return self.last_launched_app
#     #         return ""
#
#     # ------------------------
#     # Core Execution
#     # ------------------------
#     def execute_hotkey(self, keys):
#         print(f"[WindowController] Executing hotkey: {keys}")
#         pyautogui.hotkey(*keys)
#
#     # ------------------------
#     # Update last launched app
#     # ------------------------
#     def update_active_window(self, app_name: str):
#         self.last_launched_app = app_name.lower()
#
#     # ------------------------
#     # Smart Command Router
#     # ------------------------
#     def send_command(self, command: str):
#         command = command.lower().strip()
#         command = re.sub(r"[^\w\s]", "", command)
#
#         active_app = self.last_launched_app
#
#         print(f"[WindowController] Active app: {active_app}")
#         print(f"[WindowController] Heard command: {command}")
#
#         # -------- Raw Commands --------
#         if command.startswith("type "):
#             pyautogui.typewrite(command.replace("type ", "", 1), interval=0.03)
#             return True
#
#         if command.startswith("press "):
#             key = command.replace("press ", "", 1)
#             pyautogui.press(key)
#             return True
#
#         if command.startswith("hotkey "):
#             keys = command.replace("hotkey ", "").split()
#             pyautogui.hotkey(*keys)
#             return True
#
#         # -------- App-Specific Commands --------
#         if active_app and active_app in self.app_shortcuts:
#             if self._match_and_execute(command, self.app_shortcuts[active_app]):
#                 return True
#
#         # -------- Browser fallback --------
#         browser_defaults = {
#             "new tab": ["ctrl", "t"],
#             "refresh": ["ctrl", "r"],
#             "reload": ["ctrl", "r"],
#             "close tab": ["ctrl", "w"],
#         }
#
#         if self._match_and_execute(command, browser_defaults):
#             return True
#
#         # -------- Generic fallback --------
#         if self._match_and_execute(command, self.generic_shortcuts):
#             return True
#
#         return False
#
#     # ------------------------
#     # Matching Logic
#     # ------------------------
#     def _match_and_execute(self, command, shortcut_map):
#         for phrase, keys in shortcut_map.items():
#             if phrase in command:
#                 self.execute_hotkey(keys)
#                 return True
#         return False










# import subprocess
# import pyautogui
# import re
#
#
# class WindowController:
#     """App-aware window controller for Wayland/Linux using ydotool."""
#
#     def __init__(self, launcher):
#         self.launcher = launcher
#         self.last_window_name = None
#
#         # App-specific shortcuts (data only)
#         self.app_shortcuts = {
#             "code": {  # VSCode
#                 "save": ["ctrl", "s"],
#                 "run": ["ctrl", "f5"],
#                 "new file": ["ctrl", "n"],
#                 "close tab": ["ctrl", "w"],
#             },
#             "firefox": {
#                 "new tab": ["ctrl", "t"],
#                 "close tab": ["ctrl", "w"],
#                 "refresh": ["ctrl", "r"],
#                 "reload": ["ctrl", "r"],
#             },
#             "terminal": {
#                 "new tab": ["ctrl", "shift", "t"],
#                 "clear": ["ctrl", "l"],
#                 "copy": ["ctrl", "shift", "c"],
#                 "paste": ["ctrl", "shift", "v"],
#             }
#         }
#
#         # Generic fallback shortcuts
#         self.generic_shortcuts = {
#             "copy": ["ctrl", "c"],
#             "paste": ["ctrl", "v"],
#             "cut": ["ctrl", "x"],
#             "select all": ["ctrl", "a"],
#         }
#
#     # ------------------------
#     # Core Actions
#     # ------------------------
#
#     def execute_hotkey(self, keys):
#         """Send a hotkey via pyautogui or ydotool fallback."""
#         try:
#             pyautogui.hotkey(*keys)
#         except Exception as e:
#             # Fallback using ydotool (Wayland-friendly)
#             key_str = " ".join(keys)
#             subprocess.run(f"ydotool key {key_str}", shell=True, check=False)
#
#     def type_text(self, text: str):
#         try:
#             pyautogui.typewrite(text, interval=0.03)
#         except Exception:
#             subprocess.run(f'echo "{text}" | ydotool type', shell=True, check=False)
#
#     # ------------------------
#     # Smart Router
#     # ------------------------
#
#     def send_command(self, command: str):
#         """Route a command to active app or generic shortcuts."""
#         command = re.sub(r"[^\w\s]", "", command.lower().strip())
#
#         # -------- Raw commands --------
#         if command.startswith("type "):
#             self.type_text(command.replace("type ", "", 1))
#             return True
#
#         if command.startswith("press "):
#             key = command.replace("press ", "", 1)
#             self.execute_hotkey([key])
#             return True
#
#         if command.startswith("hotkey "):
#             keys = command.replace("hotkey ", "").split()
#             self.execute_hotkey(keys)
#             return True
#
#         # -------- App-Specific Commands --------
#         for app_keyword, commands in self.app_shortcuts.items():
#             if self.last_window_name and app_keyword in self.last_window_name.lower():
#                 if self._match_and_execute(command, commands):
#                     return True
#
#         # -------- Fallback Generic --------
#         if self._match_and_execute(command, self.generic_shortcuts):
#             return True
#
#         return False
#
#     # ------------------------
#     # Helper
#     # ------------------------
#
#     def _match_and_execute(self, command, shortcut_map):
#         for phrase, keys in shortcut_map.items():
#             if phrase in command:
#                 self.execute_hotkey(keys)
#                 return True
#         return False
#
#     def update_active_window(self, name: str):
#         """Set the name of the current focused window."""
#         self.last_window_name = name
