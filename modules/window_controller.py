import subprocess
import re


class WindowController:
    """OS-level hotkey controller using ydotool."""

    KEY_MAP = {
        "ctrl": "29",
        "shift": "42",
        "alt": "56",
        "tab": "15",
        "enter": "28",
        "w": "17",
        "t": "20",
        "r": "19",
        "c": "46",
        "v": "47",
        "a": "30",
        "l": "38",
        "f5": "63",
    }

    def __init__(self):
        self.last_active_app = None

        self.app_shortcuts = {
            "vscode": {
                "save": ["ctrl", "s"],
                "run": ["ctrl", "f5"],
                "new tab": ["ctrl", "t"],
                "close tab": ["ctrl", "w"],
            },
            "terminal": {
                "new tab": ["ctrl", "shift", "t"],
                "clear": ["ctrl", "l"],
                "copy": ["ctrl", "shift", "c"],
                "paste": ["ctrl", "shift", "v"],
            },
        }

        self.generic_shortcuts = {
            "copy": ["ctrl", "c"],
            "paste": ["ctrl", "v"],
            "select all": ["ctrl", "a"],
        }

    # -----------------------------
    # Active window tracking
    # -----------------------------
    def update_active_window(self, app_name: str):
        self.last_active_app = app_name

    # -----------------------------
    # Send command
    # -----------------------------
    def send_command(self, spoken_text: str) -> bool:
        spoken_text = spoken_text.lower().strip()
        spoken_text = re.sub(r"[^\w\s]", "", spoken_text)

        print(f"[WindowController] Active: {self.last_active_app}")
        print(f"[WindowController] Command: {spoken_text}")

        # App-specific
        if self.last_active_app in self.app_shortcuts:
            if self._match_and_execute(
                spoken_text,
                self.app_shortcuts[self.last_active_app]
            ):
                return True

        # Generic fallback
        if self._match_and_execute(spoken_text, self.generic_shortcuts):
            return True

        return False

    # -----------------------------
    # Match + execute
    # -----------------------------
    def _match_and_execute(self, command: str, mapping: dict) -> bool:
        for phrase, keys in mapping.items():
            if phrase in command:
                self._execute_hotkey(keys)
                return True
        return False

    # -----------------------------
    # Hotkey execution via ydotool
    # -----------------------------
    def _execute_hotkey(self, keys):
        sequence = []

        for k in keys:
            code = self.KEY_MAP.get(k)
            if code:
                sequence.append(f"{code}:1")

        for k in reversed(keys):
            code = self.KEY_MAP.get(k)
            if code:
                sequence.append(f"{code}:0")

        if sequence:
            subprocess.run(["ydotool", "key", *sequence])
