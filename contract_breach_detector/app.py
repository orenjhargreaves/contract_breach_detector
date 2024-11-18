from dotenv import load_dotenv
import os

from contract_processor import ContractProcessor

# Load environment variables from .env file
load_dotenv()

alum_file_path = f"/home/oren/Documents/Python/magentic_poc/contract_breach_detector/contracts/Aluminium_Contract.docx"
print(os.path.exists(alum_file_path))
doc_processor = ContractProcessor()

alum_document = doc_processor.load_document(alum_file_path)

terms_to_extract = {"What is the item being delivered?": "",
                    "When is it being delivered": "",
                    "How much of the item is being delivered": "",
                    "Are there any late delivery clauses": "",
                    "Are there any other clauses that incur financial penalties": ""}


alum_json = doc_processor.extract_terms(alum_document, terms_to_extract)

print(alum_json)

# print()

# print(alum_json["contract_details"])

# print(f"Q: What is the item being delivered? \n\
#             A: {alum_json["goods_details"]["description"]} \n\
#             Q: When is it being delivered? \n\
#             A: {alum_json["delivery"]["delivery_date"]} \n\
#             Q: How much of the item is being delivered? \n\
#             A: {alum_json["goods_details"]["quantity"]} \n\
#             Q: Are there any late delivery clauses? \n\
#             A: {alum_json["penalties"]["late_delivery"]} \n\
#             Q:Are there any other clauses that incur financial penalties?  \n\
#             A: {alum_json["goods_details"]["description"]}")