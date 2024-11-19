from dotenv import load_dotenv
import os

from contract_processor import ContractProcessor
from DB_code import DataBase
from breach_detector import DetectBreach
import structured_outputs

# Load environment variables from .env file
load_dotenv()


test_contracts = ["Copper_contract", "Steel_contract", "Aluminium_contract"]
doc_processor = ContractProcessor()
terms_to_extract = structured_outputs.contract_enforcement
ERP_db = DataBase('db/deliveries.json', 'db/items.json')

for i, c in enumerate(test_contracts):
    contracts_file_path = f"/home/oren/Documents/Python/magentic_poc/contract_breach_detector/contracts"
    provided_contract_file_path = f"{contracts_file_path}/provided/{c}.docx"
    highlighted_html_contract_file_path = f"{contracts_file_path}/highlighted/{c}.html"
    print(os.path.exists(provided_contract_file_path))
    doc = doc_processor.load_document(provided_contract_file_path)
    doc_structure = doc_processor.extract_terms(doc, terms_to_extract)
    breach_detector = DetectBreach(doc_structure, ERP_db)
    filtered_ERP = breach_detector.searchdb()
    print(breach_detector.compare_details(filtered_ERP))
    doc_structured_linked = doc_processor.extract_terms_with_locations(doc, fields = ["deliver_date", "contract_number", "quantity", "pallet_dimensions"])
    print(doc_structured_linked)
    doc_processor.generate_html_highlight(doc, doc_structured_linked, highlighted_html_contract_file_path)

