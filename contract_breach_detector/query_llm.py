import openai
import os
import hashlib
import pickle

class QueryLLM:
    def __init__(self, model: str = "gpt-4o-mini", cache_dir: str = "/home/oren/Documents/Python/magentic_poc/contract_breach_detector/cache"):
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)  # Ensure the cache directory exists

    def _generate_hash(self, raw_text: str) -> str:
        """
        Generate a unique hash for the document text and prompt.
        """
        return hashlib.sha256(raw_text.encode()).hexdigest()

    def _cache_path(self, hash_key: str) -> str:
        """
        Get the file path for the cached response.
        """
        return os.path.join(self.cache_dir, f"{hash_key}.pkl")

    def _load_from_cache(self, hash_key: str):
        """
        Load a response from the cache if it exists.
        """
        cache_file = self._cache_path(hash_key)
        if os.path.exists(cache_file):
            with open(cache_file, "rb") as file:
                return pickle.load(file)
        return None

    def _save_to_cache(self, hash_key: str, response):
        """
        Save a response to the cache.
        """
        cache_file = self._cache_path(hash_key)
        with open(cache_file, "wb") as file:
            pickle.dump(response, file)
    
    def query_llm(self, messages):

        key = " ".join(f"{message['role']}: {message['content']}" for message in messages)

        # Generate a hash for the message
        query_hash = self._generate_hash(key)

        # Check if the response is cached
        cached_response = self._load_from_cache(query_hash)
        if cached_response:
            print("Loaded response from cache.")
            return cached_response

        response = self.client.chat.completions.create(model=self.model, messages=messages)

        # Cache the response
        self._save_to_cache(query_hash, response)
        return response