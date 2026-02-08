import subprocess
import shlex


class AppLauncher:
    def __init__(self):
        # Map spoken names to executable paths
        self.apps = {
            "pycharm": "/opt/pycharm/bin/pycharm.sh",
            "vscode": "/opt/pycharm/bin/code",  # adjust if different
            "browser": "/usr/bin/firefox",
        }

    def open_app(self, spoken_name):
        spoken_name = spoken_name.lower()
        for key, path in self.apps.items():
            if key in spoken_name:
                print(f"[Launcher] Opening {key}...")
                try:
                    subprocess.Popen(shlex.split(path))
                except FileNotFoundError:
                    print(f"[Launcher] Executable not found: {path}")
                return
        print(f"[Launcher] App not recognized: {spoken_name}")



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
