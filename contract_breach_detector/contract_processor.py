from docx import Document
import openai
import os

class ContractProcessor:
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def load_document(self, filepath: str) -> Document:
        return Document(filepath)

    def extract_terms(self, document: Document) -> dict:
        # Example LLM prompt
        text = "\n".join([p.text for p in document.paragraphs])
        prompt = f"Extract contract terms: {text}"
        response = openai.ChatCompletion.create(model=self.model, prompt=prompt)
        return response["choices"][0]["text"]