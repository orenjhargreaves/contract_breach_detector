from dotenv import load_dotenv
import os

from contract_processor import ContractProcessor
from DB_code import DataBase
from breach_detector import DetectBreach
from query_llm import QueryLLM
import structured_outputs

# Load environment variables from .env file
load_dotenv()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

test_contracts = ["Copper_contract", "Steel_contract", "Aluminium_contract"]
llm = QueryLLM(debug=False)
doc_processor = ContractProcessor(llm)
terms_to_extract = structured_outputs.contract_enforcement
ERP_db = DataBase('db/deliveries.json', 'db/items.json')

for i, c in enumerate(test_contracts):
    print(f"\n -----------------------------------------------\n{c}")
    contracts_file_path = os.path.join(base_dir, "contracts")
    provided_contract_file_path = f"{contracts_file_path}/provided/{c}.docx"
    highlighted_html_contract_file_path = f"{contracts_file_path}/highlighted/{c}.html"
    # print(os.path.exists(provided_contract_file_path))
    doc = doc_processor.load_document(provided_contract_file_path)
    #print out the answers to the example questions provided
    exampleQ_responses = doc_processor.extract_terms(doc, structured_outputs.example_questions)
    for key, value in exampleQ_responses.items():
        print(f"Q: {key}\nA: {value}")
    print()


    doc_structure = doc_processor.extract_terms(doc, terms_to_extract)
    breach_detector = DetectBreach(doc_structure, ERP_db, llm)
    filtered_ERP = breach_detector.searchdb()
    contract_and_delivered = breach_detector.get_comparisons(filtered_ERP)
    # print(contract_and_delivered)
    for i, statement in enumerate(contract_and_delivered):
        print(f"{i+1}.  {statement}")
    print()

    breach_detail = breach_detector.analyse_comparisons(contract_and_delivered)
    # print(breach_detail)
    if breach_detail["breached"]:
        print(f"The contract has been breached: {breach_detail['breached_description']}\n")


    doc_structured_linked = doc_processor.extract_terms_with_locations(doc, fields = ["deliver_date", "contract_number", "quantity", "pallet_dimensions"])
    # print(doc_structured_linked)
    doc_processor.generate_html_highlight(doc, doc_structured_linked, highlighted_html_contract_file_path)
    print(f"An output html file containing the highlighted contract information used to assess whether the contrace has been breached can be found here: {highlighted_html_contract_file_path}")
