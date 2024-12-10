#General tests for Odhran

#would like to input to model a document and single query and get its direct quote from document
#get fuzzy score for this output when compared to what is found in the document
#same dir as app.py since it is in many ways replciating what I am currently using app.py for.
from dotenv import load_dotenv
import os
import sys
from docx import Document


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "..")))

from contract_breach_detector.modules.contract_processor import ContractProcessor
from contract_breach_detector.modules.query_llm import QueryLLM
from contract_breach_detector.modules.evidence_search import EvidenceSearch


# Load environment variables from .env file
load_dotenv()

# Define the base directory for file paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# List of test contracts to process
test_contracts = ["Copper_contract", "Steel_contract", "Aluminium_contract"]
queries = ["What is the contract number", "what is the delivery date", "what is the quantity or amount expected to be delievered in the contract"]
#initialise classes
llm = QueryLLM(debug=False)
evidence_search = EvidenceSearch(llm)
doc_processor = ContractProcessor(llm, evidence_search)
'''
print(f"-----------------------------------------------\n")

for contract_name in test_contracts:
    # Define file paths
    contracts_file_path = os.path.join(base_dir, "contract_breach_detector/contracts")
    provided_contract_file_path = os.path.join(contracts_file_path, "provided", f"{contract_name}.docx")
    highlighted_html_contract_file_path = os.path.join(contracts_file_path, "highlighted_v2", f"{contract_name}.html")
    # Load the provided contract
    doc = doc_processor.load_document(provided_contract_file_path)

    to_highlight = []
    fuzzy_findings = {}
    for q in queries:
        text_of_query_in_document = evidence_search.find_exact_text(q, doc)
        print(f"for query: {q}, llm returned: {text_of_query_in_document}")

        ld,l,r = evidence_search.find_best_fuzzy_match(text_of_query_in_document['evidence'], doc)
        to_highlight.append((l,r))
        fuzzy_findings[q] = [text_of_query_in_document['evidence'], ld,l,r]
    print()
    for k,v in fuzzy_findings.items():
        print(f"{k} evidence: {v}")
    
    doc_processor.generate_html_highlight_from_fuzz(doc, to_highlight, highlighted_html_contract_file_path)

    print(f"\nAn HTML file with highlighted contract information can be found here: {highlighted_html_contract_file_path}\n")
    print(f"-----------------------------------------------\n")


print(f"-----------------------------------------------\n")

for contract_name in test_contracts:
    # Define file paths
    contracts_file_path = os.path.join(base_dir, "contract_breach_detector/contracts")
    provided_contract_file_path = os.path.join(contracts_file_path, "provided", f"{contract_name}.docx")
    highlighted_html_contract_file_path = os.path.join(contracts_file_path, "highlighted_v2", f"{contract_name}.html")
    # Load the provided contract
    doc = doc_processor.load_document(provided_contract_file_path)

    to_highlight = []
    fuzzy_findings = {}
    for q in queries:
        text_of_query_in_document = evidence_search.find_exact_text(q, doc)
        print(f"for query: {q}, llm returned: {text_of_query_in_document}")
        best_match_res = evidence_search.find_best_match_in_document(text_of_query_in_document['evidence'], doc, threshold=95)
        matched_text = best_match_res[0]
        print(f"matching: {text_of_query_in_document['evidence']} to {matched_text}")
        print(best_match_res)
        if matched_text:
            print(matched_text,len(matched_text), type(matched_text))
            print(text_of_query_in_document['evidence'],len(text_of_query_in_document['evidence']), type(text_of_query_in_document['evidence']))
            # ld_score = evidence_search.calculate_levenshtein_distance(text_of_query_in_document['evidence'], matched_text)
            ld_score=9
        else:
            ld_score = None
        #add to fuzzy findings[query] the llm output, ld_score, start_index and end_index
        fuzzy_findings[q] = [text_of_query_in_document['evidence'], ld_score,best_match_res[2],best_match_res[3]]
    print()
    for k,v in fuzzy_findings.items():
        print(f"{k} evidence: {v}")
    print(f"-----------------------------------------------\n")
'''
print(f"-----------------------------------------------\n")

for contract_name in test_contracts:
    # Define file paths
    contracts_file_path = os.path.join(base_dir, "contract_breach_detector/contracts")
    provided_contract_file_path = os.path.join(contracts_file_path, "provided", f"{contract_name}.docx")
    highlighted_html_contract_file_path = os.path.join(contracts_file_path, "highlighted_v2", f"{contract_name}.html")
    # Load the provided contract
    doc = doc_processor.load_document(provided_contract_file_path)

    to_highlight = []
    fuzzy_findings = {}
    for q in queries:
        text_of_query_in_document = evidence_search.find_exact_text(q, doc)
        print(f"for query: {q}, llm returned: {text_of_query_in_document}")
        best_match_res = evidence_search.find_best_match_in_document_v2(text_of_query_in_document['evidence'], doc)
        matched_text = best_match_res[0]
        #add to fuzzy findings[query] the llm output, best_match, ld_score, start_index and end_index
        fuzzy_findings[q] = [text_of_query_in_document['evidence'], best_match_res[0], best_match_res[1],best_match_res[2],best_match_res[3]]
    print()
    for k,v in fuzzy_findings.items():
        print(f"{k} evidence: {v}")
    print(f"-----------------------------------------------\n")

# doc = Document()
# doc.add_paragraph("This is a test contract.")
# a = evidence_search.find_best_match_in_document_v2("text ctract", doc, threshold=45)
# print(a)