from sentence_transformers import SentenceTransformer
import faiss
import os
import yaml
# Example with HuggingFace local LLM
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import whisper


class Brain:
    def __init__(self, config_path="./config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        # self.model_path = self.config['llm']['model_path']
        model_name = 'base'  # 'tiny.en' change llm model here
        self.model = whisper.load_model(model_name, device="cpu")

        print(f"Loading local LLM from {model_name}...")
        # self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        # self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        # self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        #
        # # FAISS memory
        # self.vector_db = faiss.IndexFlatL2(768) # Placeholder dimension
        # self.memory_texts = []

    def add_memory(self, text):
        # Convert text to vector and add
        from sentence_transformers import SentenceTransformer
        encoder = SentenceTransformer('all-MiniLM-L6-v2')
        vec = encoder.encode([text])
        self.vector_db.add(vec)
        self.memory_texts.append(text)

    def query_memory(self, query):
        if len(self.memory_texts) == 0:
            return []
        encoder = SentenceTransformer('all-MiniLM-L6-v2')
        q_vec = encoder.encode([query])
        D, I = self.vector_db.search(q_vec, k=5)
        return [self.memory_texts[i] for i in I[0]]

    def create_plan(self, intent: str):
        print(f"Brain received intent: {intent}")
        return {
            "summary": f"I plan to handle: {intent}",
            "tasks": [{"action": "create_file", "filename": "main.py", "content": "print('Hello World')"}]
        }



# from sentence_transformers import SentenceTransformer
# Example with HuggingFace local LLM
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# import faiss
# import os
# import yaml


# class Brain:
#     def __init__(self):
#         print("Brain (mock) initialized.")
#
#     def create_plan(self, intent: str):
#         print(f"Brain received intent: {intent}")
#         return {
#             "summary": f"I plan to handle: {intent}",
#             "tasks": [{"action": "create_file", "filename": "main.py", "content": "print('Hello World')"}]
#         }


# class Brain:
#     def __init__(self):
        # with open(config_path, "r") as f:
        #     self.config = yaml.safe_load(f)
        # self.model_path = self.config['llm']['model_path']
        #
        # print(f"Loading local LLM from {self.model_path}...")
        # self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        # self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        # self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        #
        # # FAISS memory
        # self.vector_db = faiss.IndexFlatL2(768)  # Placeholder dimension
        # self.memory_texts = []
        # print("Brain (mock) initialized.")

    # def add_memory(self, text):
        # Convert text to vector
    #     encoder = SentenceTransformer('all-MiniLM-L6-v2')
    #     vec = encoder.encode([text])
    #     self.vector_db.add(vec)
    #     self.memory_texts.append(text)
    #     print("Memory added.")
    #
    # def query_memory(self, query):
    #     if len(self.memory_texts) == 0:
    #         return []
    #     encoder = SentenceTransformer('all-MiniLM-L6-v2')
    #     q_vec = encoder.encode([query])
    #     D, I = self.vector_db.search(q_vec, k=5)
    #     return [self.memory_texts[i] for i in I[0]]

    # def create_plan(self, intent: str):
    #     # Query memory for context
    #     # context = self.query_memory(intent)
    #     # prompt = f"Context: {context}\nUser intent: {intent}\nPlan steps:"
    #     # result = self.generator(prompt, max_length=200)[0]['generated_text']
    #     # self.add_memory(f"Plan for '{intent}': {result}")
    #     print(f"Brain received intent: {intent}")
    #     return {
    #         "summary": result,
    #         "tasks": [
    #             {"action": "create_file", "filename": "main.py", "content": "print('Hello World')"}
    #         ]
    #     }


    # MOCK
    # def create_plan(self, intent: str):
    #     print(f"Brain received intent: {intent}")
    #     return {
    #         "summary": f"I plan to: {intent}",
    #         "tasks": [{"action": "create_file", "filename": "main.py", "content": "print('Hello World')"}]
    #     }
