import duckdb

# Connect to an in-memory DuckDB database
con = duckdb.connect()

# Register the JSON files as tables
con.execute(
    "CREATE VIEW deliveries AS SELECT * FROM read_json_auto('db/deliveries.json');"
)
con.execute("CREATE VIEW items AS SELECT * FROM read_json_auto('db/items.json');")

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

result = con.execute(query).fetchdf()
print(result)
