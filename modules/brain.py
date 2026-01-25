class Brain:
    def __init__(self):
        print("Brain (mock) initialized.")

    def create_plan(self, intent: str):
        print(f"Brain received intent: {intent}")
        return {
            "summary": f"I plan to: {intent}",
            "tasks": [{"action": "create_file", "filename": "main.py", "content": "print('Hello World')"}]
        }
