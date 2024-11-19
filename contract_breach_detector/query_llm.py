import openai, os, hashlib, pickle, json, re

class QueryLLM:
    def __init__(self, debug=False, model: str = "gpt-4o-mini", cache_dir: str = "/home/oren/Documents/Python/magentic_poc/contract_breach_detector/cache"):
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)  # Ensure the cache directory exists
        self.debug = debug

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
    
    def _extract_json(self, content):
        """
        Extracts and parses JSON content from the OpenAI response.
        Handles cases where the JSON is wrapped in triple backticks.
        """
        # Regular expression to find JSON content, optionally wrapped in backticks
        json_match = re.search(r"```json\n(.*?)```|({.*})", content, re.DOTALL)
        
        if json_match:
            json_content = json_match.group(1) or json_match.group(2)  # Extract JSON portion
            try:
                return json.loads(json_content)  # Parse JSON
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                print("Extracted content:", json_content)
                raise
        else:
            raise ValueError("No JSON object found in the response content.")
    
    def query_llm(self, messages):

        key = " ".join(f"{message['role']}: {message['content']}" for message in messages)

        # Generate a hash for the message
        query_hash = self._generate_hash(key)

        # Check if the response is cached
        cached_output = self._load_from_cache(query_hash)
        if cached_output:
            
            if self.debug:
                print("Loaded response from cache.")
                print(cached_output)
            return cached_output

        response = self.client.chat.completions.create(model=self.model, messages=messages)
        
        if self.debug:
            print(response)

        output = self._extract_json(response.choices[0].message.content)

        # Cache the response
        self._save_to_cache(query_hash, output)

        

        return output