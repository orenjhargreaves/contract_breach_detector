from dotenv import load_dotenv
import os

from contract_processor import ContractProcessor
from DB_code import DataBase
from breach_detector import DetectBreach
import structured_outputs

# Load environment variables from .env file
load_dotenv()

alum_file_path = f"/home/oren/Documents/Python/magentic_poc/contract_breach_detector/contracts/Aluminium_Contract.docx"
print(os.path.exists(alum_file_path))
doc_processor = ContractProcessor()

alum_document = doc_processor.load_document(alum_file_path)

terms_to_extract = structured_outputs.contract_enforcement


alum_json = doc_processor.extract_terms(alum_document, terms_to_extract)

# for i in alum_json.items():
#     print(i)

ERP_db = DataBase('db/deliveries.json', 'db/items.json')
# print(contract_db.original_example_query())

breach_detector = DetectBreach(alum_json, ERP_db)
alum_ERP = breach_detector.searchdb()
breach_detector.compare_details(alum_ERP)
