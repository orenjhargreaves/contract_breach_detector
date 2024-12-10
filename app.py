from dotenv import load_dotenv
import os
import sys
from docx import Document

# Add the parent directory of this script to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "..")))
from contract_breach_detector.modules.contract_processor import ContractProcessor
from contract_breach_detector.modules.DB_code import DataBase
from contract_breach_detector.modules.breach_detector import DetectBreach
from contract_breach_detector.modules.query_llm import QueryLLM
import contract_breach_detector.modules.structured_outputs as structured_outputs
from contract_breach_detector.modules.evidence_search import EvidenceSearch

# Load environment variables from .env file
load_dotenv()

# Define the base directory for file paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# List of test contracts to process
test_contracts = ["Copper_contract", "Steel_contract", "Aluminium_contract"]

# Initialize the LLM, document processor, and database
llm = QueryLLM(debug=True)
doc_processor = ContractProcessor(llm)
terms_to_extract = structured_outputs.contract_enforcement
ERP_db = DataBase('db/deliveries.json', 'db/items.json')
evidence_search = EvidenceSearch(llm)

for i, contract_name in enumerate([test_contracts[0]]):

    # Define file paths
    contracts_file_path = os.path.join(base_dir, "contract_breach_detector/contracts")
    provided_contract_file_path = os.path.join(contracts_file_path, "provided", f"{contract_name}.docx")
    highlighted_html_contract_file_path = os.path.join(contracts_file_path, "highlighted", f"{contract_name}.html")

    # Load the provided contract
    doc = doc_processor.load_document(provided_contract_file_path)

    test = evidence_search.find_exact_text(" contract number1415738", doc)

    print(test)

    s,l,r = evidence_search.find_best_fuzzy_match(test['evidence'], doc)

    print(s,l,r)

    doc_processor.generate_html_highlight_from_fuzz(doc, [(l,r)], highlighted_html_contract_file_path)

    # test_doc = Document()
    # test_doc.add_paragraph("This is a test contract. specific piece of information to be returned: password123. Rest of the test contract")

    # test2 = evidence_search.find_exact_text(text="specific piece of information: password123", document=test_doc)

    # print(test2)


















#commenting out below while testing evidence_search
"""
# Process each contract
for i, contract_name in enumerate(test_contracts):
    print(f"-----------------------------------------------\n{contract_name}")

    # Define file paths
    contracts_file_path = os.path.join(base_dir, "contract_breach_detector/contracts")
    provided_contract_file_path = os.path.join(contracts_file_path, "provided", f"{contract_name}.docx")
    highlighted_html_contract_file_path = os.path.join(contracts_file_path, "highlighted", f"{contract_name}.html")

    # Load the provided contract
    doc = doc_processor.load_document(provided_contract_file_path)

    # Extract and display responses to example questions
    exampleQ_responses = doc_processor.extract_terms(doc, structured_outputs.example_questions)
    print("Responses to Example Questions:")
    for key, value in exampleQ_responses.items():
        print(f"Q: {key}\nA: {value}")
    print()

    # Extract structured contract terms
    doc_structure = doc_processor.extract_terms(doc, terms_to_extract)

    # Initialize breach detector
    breach_detector = DetectBreach(doc_structure, ERP_db, llm)

    # Search the ERP database for contract details
    filtered_ERP = breach_detector.searchdb()

    # Generate and display comparisons between contract and delivered values
    contract_and_delivered = breach_detector.get_comparisons(filtered_ERP)
    print("Contract vs Delivered Comparisons:")
    for i, statement in enumerate(contract_and_delivered):
        print(f"{i+1}. {statement}")
    print()

    # Analyze the comparisons for breaches
    breach_detail = breach_detector.analyse_comparisons(contract_and_delivered)
    if breach_detail["breached"]:
        print(f"The contract has been breached: {breach_detail['breached_description']}\n")

    # Extract terms with locations and generate an HTML-highlighted contract
    doc_structured_linked = doc_processor.extract_terms_with_locations(
        doc, fields=["deliver_date", "contract_number", "quantity", "pallet_dimensions"]
    )
    doc_processor.generate_html_highlight(doc, doc_structured_linked, highlighted_html_contract_file_path)
    print(f"An HTML file with highlighted contract information can be found here: {highlighted_html_contract_file_path}\n")
print(f"-----------------------------------------------\n")
"""