import subprocess
import shlex
import os


class AppLauncher:
    def __init__(self):
        self.apps = {
            "pycharm": {
                "path": "/opt/pycharm-community-2025.3.1/bin/pycharm.sh",
                "aliases": [
                    "pycharm",
                    "idea",
                    "jetbrains",
                    "open pycharm",
                    "launch pycharm",
                    "python"
                ],
            },
            "vscode": {
                "path": "/usr/bin/code",
                "aliases": [
                    "vscode",
                    "visual studio code",
                    "code editor",
                    "launch vscode",
                    "code"
                ],
            },
            "browser": {
                "path": "/usr/bin/firefox",
                "aliases": [
                    "firefox",
                    "browser",
                    "open browser",
                    "launch firefox",
                    "Bowser"
                ],
            },
            "terminal": {
                "path": "/usr/bin/gnome-terminal",
                "aliases": [
                    "terminal",
                    "shell",
                    "open terminal",
                    "launch terminal",
                ],
            },
        }

    def open_app(self, spoken_text: str) -> bool:
        spoken_text = spoken_text.lower()

        for app_name, app_info in self.apps.items():
            for alias in app_info["aliases"]:
                if alias in spoken_text:
                    print(f"[Launcher] Launching {app_name}...")
                    os.system(f'"{app_info["path"]}" &')
                    return True

        print(f"[Launcher] App not recognized in: {spoken_text}")
        return False




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
