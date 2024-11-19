import duckdb

class DataBase:
    """
    A class to interact with a DuckDB in-memory database that processes JSON data
    related to deliveries and items.

    Attributes:
        con (duckdb.DuckDBPyConnection): A connection to the DuckDB database.
    """

    def __init__(self, deliveries_path: str, items_path: str):
        """
        Initializes the database by connecting to an in-memory DuckDB instance 
        and registering JSON files as database tables.

        Args:
            deliveries_path (str): The path to the deliveries JSON file.
            items_path (str): The path to the items JSON file.
        """
        self.con = duckdb.connect()  # Connect to an in-memory DuckDB database

        # Register the JSON files as tables
        self.con.execute(
            f"CREATE VIEW deliveries AS SELECT * FROM read_json_auto('{deliveries_path}');"
        )
        self.con.execute(
            f"CREATE VIEW items AS SELECT * FROM read_json_auto('{items_path}');"
        )

    def query_db(self, query: str):
        """
        Executes a SQL query on the database and fetches the result as a DataFrame.

        Args:
            query (str): The SQL query to execute.

        Returns:
            pandas.DataFrame: The result of the SQL query.
        """
        return self.con.execute(query).fetchdf()

    def lookup_contract(self, query_contract_number: str):
        """
        Looks up contract details in the database based on the given contract number.

        Args:
            query_contract_number (str): The contract number to search for.

        Returns:
            pandas.DataFrame: A DataFrame containing the details of the contract.
        """
        query = f"""
        SELECT d.*, i.*
        FROM deliveries d
        JOIN items i
        ON d.delivery_id = i.delivery_id
        WHERE i.contract_number = '{query_contract_number}';
        """
        return self.query_db(query)
