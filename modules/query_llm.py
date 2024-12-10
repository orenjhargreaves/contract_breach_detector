import openai
import os
import hashlib
import pickle
import json
import re


class QueryLLM:
    """
    A class for interacting with an LLM (Large Language Model) such as OpenAI's GPT, 
    with caching support to avoid redundant queries and ensure efficient usage.

    Attributes:
        model (str): The model to be used for querying the LLM.
        client (openai.OpenAI): The OpenAI client for interacting with the API.
        cache_dir (str): Directory to store cached responses.
        debug (bool): Flag for enabling debug mode.
    """

    def __init__(self, debug=False, model: str = "gpt-4o-mini", cache_dir: str = "./cache"):
        """
        Initializes the QueryLLM class.

        Args:
            debug (bool): Enable or disable debug mode (default is False).
            model (str): The model to use for querying the LLM (default is "gpt-4o-mini").
            cache_dir (str): Directory to store cached responses (default is "./cache").
        """
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)  # Ensure the cache directory exists
        self.debug = debug

    def _generate_hash(self, raw_text: str) -> str:
        """
        Generates a unique hash for the given raw text.

        Args:
            raw_text (str): The raw text to hash.

        Returns:
            str: A SHA256 hash of the input text.
        """
        return hashlib.sha256(raw_text.encode()).hexdigest()

    def _cache_path(self, hash_key: str) -> str:
        """
        Constructs the file path for the cached response based on the hash key.

        Args:
            hash_key (str): The hash key for the cache.

        Returns:
            str: The full path to the cache file.
        """
        return os.path.join(self.cache_dir, f"{hash_key}.pkl")

    def _load_from_cache(self, hash_key: str):
        """
        Loads a cached response if it exists.

        Args:
            hash_key (str): The hash key for the cache.

        Returns:
            object: The cached response or None if not found.
        """
        cache_file = self._cache_path(hash_key)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "rb") as file:
                    return pickle.load(file)
            except (EOFError, pickle.UnpicklingError):
                # Handle empty or corrupted cache file
                if self.debug:
                    print(f"Cache file {cache_file} is corrupted or empty. Deleting...")
                os.remove(cache_file)
        return None

    def _save_to_cache(self, hash_key: str, response):
        """
        Saves a response to the cache.

        Args:
            hash_key (str): The hash key for the cache.
            response (object): The response to cache.
        """
        cache_file = self._cache_path(hash_key)
        with open(cache_file, "wb") as file:
            pickle.dump(response, file)

    def _extract_json(self, content: str) -> dict:
        """
        Extracts and parses JSON content from the LLM response.

        Handles cases where the JSON is wrapped in triple backticks 
        or uses single quotes instead of double quotes.

        Args:
            content (str): The content from the LLM response.

        Returns:
            dict: The parsed JSON content.

        Raises:
            ValueError: If no valid JSON object is found in the content.
            json.JSONDecodeError: If JSON parsing fails after attempts to fix formatting.
        """
        # Regular expression to find JSON content, optionally wrapped in backticks
        json_match = re.search(r"```json\n(.*?)```|({.*})", content, re.DOTALL)

        if json_match:
            json_content = json_match.group(1) or json_match.group(2)  # Extract JSON portion
            try:
                # Try to parse as valid JSON
                return json.loads(json_content)
            except json.JSONDecodeError:
                if self.debug:
                    print("Attempting to fix JSON with single quotes...")
                try:
                    # Handle single-quoted JSON-like content
                    fixed_content = json_content.replace("'", '"')
                    return json.loads(fixed_content)
                except json.JSONDecodeError as e:
                    if self.debug:
                        print("Error parsing JSON after fixing:", e)
                        print("Extracted content:", json_content)
                    raise
        else:
            raise ValueError("No JSON object found in the response content.")

    def query_llm(self, messages: list) -> dict:
        """
        Queries the LLM with the provided messages.

        If a cached response exists for the same query, it will be loaded from the cache.
        Otherwise, the query will be sent to the LLM, and the response will be cached.

        Args:
            messages (list): A list of message dictionaries to send to the LLM.

        Returns:
            dict: The parsed JSON response from the LLM or cache.
        """
        # Construct a unique key for the query
        key = " ".join(f"{message['role']}: {message['content']}" for message in messages)

        # Generate a hash for the query
        query_hash = self._generate_hash(key)

        # Check if the response is cached
        cached_output = self._load_from_cache(query_hash)
        if cached_output:
            if self.debug:
                print("Loaded response from cache.")
                print(cached_output)
            return cached_output

        # Send the query to the LLM
        response = self.client.chat.completions.create(model=self.model, messages=messages, temperature=0)

        if self.debug:
            print("LLM Response:", response)

        # Extract and parse the JSON content
        output = self._extract_json(response.choices[0].message.content)

        # Cache the response
        self._save_to_cache(query_hash, output)

        return output
