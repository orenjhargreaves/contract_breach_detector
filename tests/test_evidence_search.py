import unittest
from unittest.mock import patch, MagicMock

from docx import Document

from contract_breach_detector.modules.evidence_search import EvidenceSearch
from contract_breach_detector.modules.query_llm import QueryLLM


class TestEvidenceSearch(unittest.TestCase):
    """
    Test suite for the EvidenceSearch class.
    """

    def setUp(self):
        """
        Sets up the test environment by mocking the QueryLLM instance
        and creating a ContractProcessor instance.
        """
        self.mock_llm = MagicMock(spec=QueryLLM)
        self.evidence_search = EvidenceSearch(self.mock_llm)

        # Create a temporary test document
        self.test_document = Document()
        self.test_document.add_paragraph("This is a test contract which contains lots of important contractual data. The Head of Purchasing is Sean Cousins. Rest of the test contract")

    def test_find_exact_text(self):
        """
        Tests the find_exact_text method to ensure it queries the LLM
        and returns the expected exact text.
        """

        # Mock comparisons list
        text_to_find = "Head of Purchasing: Sean Cousins"

        # Mock LLM response
        mock_llm_response = {
            "evidence": (
                "The Head of Purchasing is Sean Cousins"
            ),
        }
        self.mock_llm.query_llm.return_value = mock_llm_response

        # Test the method
        result = self.evidence_search.find_exact_text(text=text_to_find, document=self.test_document)

        self.mock_llm.query_llm.assert_called_once()  # Ensure LLM was called
        self.assertEqual(result, mock_llm_response)  # Ensure result matches mock response
    
    def test_find_best_fuzzy_match(self):
        """
        Tests the find_best_fuzzy_match method to ensure the correct location is found.
        """
        text_to_find = "The Head of Purchasing is Sean Cousins"
        correct_pointers = (75,113)
        
        result = self.evidence_search.find_best_fuzzy_match(text_to_find, self.test_document)
        result_pointers = (result[1], result[2])
        self.assertEqual(result_pointers, correct_pointers)

