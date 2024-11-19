import unittest
from unittest.mock import patch, MagicMock
import json
import os
import shutil
import pickle
from contract_breach_detector.modules.query_llm import QueryLLM


class TestQueryLLM(unittest.TestCase):
    """
    Test suite for the QueryLLM class with mocked OpenAI client.
    """

    @patch("contract_breach_detector.modules.query_llm.openai.OpenAI")
    def setUp(self, mock_openai):
        """
        Sets up the test environment for QueryLLM.
        """
        # Configure the mock OpenAI client
        self.mock_openai = mock_openai
        self.test_cache_dir = os.path.join(os.path.dirname(__file__), "test_data", "test_cache")
        os.makedirs(self.test_cache_dir, exist_ok=True)
        self.mock_openai.return_value.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=json.dumps({"response": "Mocked response"})))]
        )

        # Initialize QueryLLM with the mocked client
        self.cache_dir = os.path.join(os.path.dirname(__file__), "test_data", "test_cache")
        self.query_llm = QueryLLM(debug=True, cache_dir=self.cache_dir)

        # Clean up the cache directory
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def tearDown(self):
        """
        Clean up after tests by removing the test cache directory.
        """
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)

    def test_query_llm_with_cache(self):
        """
        Test query_llm method uses the cache if a query has been made before.
        """
        messages = [{"role": "user", "content": "What are Newton's laws of motion?"}]
        query_hash = self.query_llm._generate_hash(" ".join(f"{msg['role']}: {msg['content']}" for msg in messages))
        cache_file = self.query_llm._cache_path(query_hash)

        # Simulate saving to cache
        with open(cache_file, "wb") as file:
            pickle.dump({"response": "Cached response"}, file)

        # Test retrieving from cache
        response = self.query_llm.query_llm(messages)
        self.assertEqual(response, {"response": "Cached response"})  # Ensure the cached response is returned

    def test_query_llm_without_cache(self):
        """
        Test query_llm method when the cache is empty, and a query is sent to the LLM.
        """
        messages = [{"role": "user", "content": "What are Newton's laws of motion?"}]
        response = self.query_llm.query_llm(messages)
        self.assertEqual(response["response"], "Mocked response")
        self.mock_openai.return_value.chat.completions.create.assert_called_once()

    def test_extract_json(self):
        """
        Test the _extract_json method to ensure it correctly parses JSON from content.
        """
        json_content = """```json
        {
            "response": "Extracted JSON response"
        }
        ```"""
        result = self.query_llm._extract_json(json_content)
        self.assertEqual(result["response"], "Extracted JSON response")

    def test_extract_json_with_single_quotes(self):
        """
        Test _extract_json method for JSON content with single quotes.
        """
        json_content = """{
            'response': 'Single quoted JSON response'
        }"""
        result = self.query_llm._extract_json(json_content)
        self.assertEqual(result["response"], "Single quoted JSON response")

    def test_cache_saving_and_loading(self):
        """
        Test the caching mechanism for saving and loading responses.
        """
        hash_key = "test_hash_key"
        cache_data = {"response": "Cached response"}
        self.query_llm._save_to_cache(hash_key, cache_data)

        # Verify that the cache can be loaded
        loaded_data = self.query_llm._load_from_cache(hash_key)
        self.assertEqual(loaded_data, cache_data)

        # Clean up the cache
        os.remove(self.query_llm._cache_path(hash_key))


if __name__ == "__main__":
    unittest.main()