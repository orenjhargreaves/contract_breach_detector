import duckdb

class DataBase:
    def __init__(self, deliveries_path, items_path):
        # Connect to an in-memory DuckDB database
        self.con = duckdb.connect()

        # Register the JSON files as tables
        self.con.execute(
            "CREATE VIEW deliveries AS SELECT * FROM read_json_auto('db/deliveries.json');"
        )
        self.con.execute("CREATE VIEW items AS SELECT * FROM read_json_auto('db/items.json');")
    
    def query_db(self, query):
        return self.con.execute(query).fetchdf()
    
    def lookup_contract(self, query_contract_number):
        query = f"""
        SELECT d.*, i.*
        FROM deliveries d
        JOIN items i
        ON d.delivery_id = i.delivery_id
        WHERE i.contract_number = '{query_contract_number}'
        ;
        """
        return self.query_db(query)
    
    def original_example_query(self):
        # Example Query: Get all items from deliveries that are 'In Transit'
        query = """
        SELECT 
            d.delivery_id, 
            d.delivery_date, 
            d.supplier, 
            i.item_id, 
            i.material_number, 
            i.description, 
            i.quantity
        FROM 
            deliveries d
        JOIN 
            items i 
        ON 
            d.delivery_id = i.delivery_id
        WHERE 
            d.supplier = 'AluMetals';
        """
        return self.query_db(query)
