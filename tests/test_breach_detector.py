import unittest
from unittest.mock import MagicMock
from contract_breach_detector.contract_breach_detector.breach_detector import DetectBreach
from contract_breach_detector.contract_breach_detector.DB_code import DataBase
from contract_breach_detector.contract_breach_detector.query_llm import QueryLLM


class TestDetectBreach(unittest.TestCase):
    """
    Test suite for the DetectBreach class.
    """

    def setUp(self):
        """
        Sets up the test environment by mocking the database and LLM instances,
        and creating a DetectBreach instance with a test contract.
        """
        self.mock_db = MagicMock(spec=DataBase)
        self.mock_llm = MagicMock(spec=QueryLLM)
        self.test_contract = {
            "info": {"contract_number": "12345"},
            "details": {
                "delivery_date": "2024-06-15",
                "quantity": "10",
                "pallet_dimensions": "1200x1000x150",
            },
        }
        self.detect_breach = DetectBreach(self.test_contract, self.mock_db, self.mock_llm)

    def test_searchdb(self):
        """
        Tests the searchdb method to ensure it retrieves contract information from the database.
        """
        # Mock database response
        mock_erp_info = {
            "delivery_date": ["2024-06-15"],
            "quantity": ["10"],
            "pallet_dimensions": ["1200x1000x150"],
        }
        self.mock_db.lookup_contract.return_value = mock_erp_info

        # Test the method
        result = self.detect_breach.searchdb()

        self.mock_db.lookup_contract.assert_called_once_with("12345")  # Ensure DB was queried
        self.assertEqual(result, mock_erp_info)  # Ensure result matches mock response

    def test_get_comparisons(self):
        """
        Tests the get_comparisons method to ensure it generates the correct comparisons.
        """
        # Mock ERP info
        mock_erp_info = {
            "delivery_date": ["2024-06-15"],
            "quantity": ["12"],  # Example of a mismatch
            "pallet_dimensions": ["1200x1000x150"],
        }

        # Test the method
        comparisons = self.detect_breach.get_comparisons(mock_erp_info)

        expected_comparisons = [
            "The contract states that the value for delivery_date should be 2024-06-15. "
            "The delivered value was 2024-06-15.",
            "The contract states that the value for quantity should be 10. "
            "The delivered value was 12.",
            "The contract states that the value for pallet_dimensions should be 1200x1000x150. "
            "The delivered value was 1200x1000x150.",
        ]

        self.assertEqual(comparisons, expected_comparisons)

    def test_analyse_comparisons(self):
        """
        Tests the analyse_comparisons method to ensure it queries the LLM
        and returns the expected analysis results.
        """
        # Mock comparisons list
        mock_comparisons = [
            "The contract states that the value for delivery_date should be 2024-06-15. "
            "The delivered value was 2024-06-15.",
            "The contract states that the value for quantity should be 10. "
            "The delivered value was 12.",
        ]

        # Mock LLM response
        mock_llm_response = {
            "breached": True,
            "breached_description": (
                "The quantity was delivered as 12, which exceeds the contractual value of 10. "
                "This is a breach."
            ),
        }
        self.mock_llm.query_llm.return_value = mock_llm_response

        # Test the method
        result = self.detect_breach.analyse_comparisons(mock_comparisons)

        self.mock_llm.query_llm.assert_called_once()  # Ensure LLM was called
        self.assertEqual(result, mock_llm_response)  # Ensure result matches mock response


if __name__ == "__main__":
    unittest.main()
