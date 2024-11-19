import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from contract_breach_detector.modules.DB_code import DataBase


class TestDataBase(unittest.TestCase):
    """
    Test suite for the DataBase class.
    """

    def setUp(self):
        """
        Sets up the test environment by mocking the database connection
        and creating a DataBase instance.
        """
        self.deliveries_path = "db/deliveries.json"
        self.items_path = "db/items.json"
        
        # Patch the DuckDB connection and initialize the DataBase instance
        patcher = patch("contract_breach_detector.modules.DB_code.duckdb.connect")
        self.mock_connect = patcher.start()
        self.addCleanup(patcher.stop)

        self.mock_connection = self.mock_connect.return_value
        self.mock_execute = self.mock_connection.execute
        self.database = DataBase(self.deliveries_path, self.items_path)

    def test_initialization(self):
        """
        Tests that the DataBase class correctly initializes and registers tables.
        """
        # Check that the DuckDB connection was created
        self.mock_connect.assert_called_once()

        # Check that the JSON files were registered as views
        self.mock_execute.assert_any_call(
            f"CREATE VIEW deliveries AS SELECT * FROM read_json_auto('{self.deliveries_path}');"
        )
        self.mock_execute.assert_any_call(
            f"CREATE VIEW items AS SELECT * FROM read_json_auto('{self.items_path}');"
        )

    def test_query_db(self):
        """
        Tests the query_db method to ensure it executes SQL queries correctly.
        """
        # Mock query results
        mock_df = pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})
        self.mock_execute.return_value.fetchdf.return_value = mock_df

        query = "SELECT * FROM deliveries;"
        result = self.database.query_db(query)

        # Check that the correct query was executed
        self.mock_execute.assert_any_call(query)  # Ensure the specific query was executed

        # Check that the result matches the mock
        pd.testing.assert_frame_equal(result, mock_df)

    def test_lookup_contract(self):
        """
        Tests the lookup_contract method to ensure it retrieves the correct contract data.
        """
        # Mock contract lookup result
        mock_df = pd.DataFrame({
            "delivery_id": [1],
            "delivery_date": ["2024-06-15"],
            "supplier": ["Test Supplier"],
            "item_id": [101],
            "material_number": ["M001"],
            "description": ["Test Material"],
            "quantity": [10],
            "contract_number": ["12345"]
        })
        self.mock_execute.return_value.fetchdf.return_value = mock_df

        # Reset mock after setup to isolate test-specific queries
        self.mock_execute.reset_mock()

        query_contract_number = "12345"
        result = self.database.lookup_contract(query_contract_number)

        expected_query = f"""
        SELECT d.*, i.*
        FROM deliveries d
        JOIN items i
        ON d.delivery_id = i.delivery_id
        WHERE i.contract_number = '{query_contract_number}';
        """

        # Normalize the expected query
        normalized_expected_query = " ".join(expected_query.split())

        # Extract the actual query from the mock calls
        actual_query = None
        for call in self.mock_execute.call_args_list:
            if "SELECT" in call.args[0]:
                actual_query = " ".join(call.args[0].split())
                break

        # Verify the query matches
        self.assertEqual(normalized_expected_query, actual_query)

        # Verify the result matches the mock
        pd.testing.assert_frame_equal(result, mock_df)


if __name__ == "__main__":
    unittest.main()
