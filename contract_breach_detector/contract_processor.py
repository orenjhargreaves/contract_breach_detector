from docx import Document
from query_llm import QueryLLM
import openai
import os
import pickle
import json
import hashlib

# extracted_terms_format = {
#   "contract_details": {
#     "contract_number": "",
#     "commencement_date": "",
#     "parties": {
#       "customer": {
#         "name": "",
#         "address": "",
#         "representative": ""
#       },
#       "supplier": {
#         "name": "",
#         "address": "",
#         "vat_number": "",
#         "representative": ""
#       }
#     }
#   },
#   "goods_details": {
#     "description": "",
#     "quantity": "",
#     "specifications": {
#       "dimensions": "",
#       "material_composition": "",
#       "quality_standards": "",
#       "surface_finish": "",
#       "mechanical_properties": "",
#       "flatness_tolerance": "",
#       "compliance_and_certifications": {
#         "regulatory_compliance": "",
#         "certification": ""
#       }
#     }
#   },
#   "delivery": {
#     "delivery_date": "",
#     "delivery_location": "",
#     "packaging": {
#       "palletization": "",
#       "labeling": "",
#       "handling_instructions": ""
#     },
#     "penalties": {
#       "late_delivery": {
#         "penalty_rate": "",
#         "maximum_penalty": "",
#         "termination_threshold": ""
#       }
#     }
#   },
#   "price_and_payment": {
#     "contract_price": "",
#     "payment_terms": "",
#     "taxes_and_duties": "",
#     "set_off_rights": ""
#   },
#   "warranties": {
#     "warranty_period": "",
#     "warranty_conditions": "",
#     "remedies_for_breach": ""
#   },
#   "liability_and_indemnification": {
#     "limitation_of_liability": "",
#     "cap_on_liability": "",
#     "supplier_indemnification": "",
#     "insurance": ""
#   },
#   "termination": {
#     "termination_for_convenience": "",
#     "termination_for_cause": {
#       "breach_period": "",
#       "bankruptcy": ""
#     },
#     "consequences_of_termination": ""
#   },
#   "force_majeure": {
#     "definition": "",
#     "effect": "",
#     "obligations": "",
#     "termination_due_to_prolonged_event": ""
#   },
#   "confidentiality": {
#     "scope": "",
#     "obligations": "",
#     "exclusions": "",
#     "return_or_destruction": ""
#   },
#   "intellectual_property": {
#     "ownership": "",
#     "license_grant": "",
#     "indemnity": ""
#   },
#   "dispute_resolution": {
#     "negotiation": "",
#     "mediation": "",
#     "arbitration": {
#       "rules": "",
#       "seat_of_arbitration": "",
#       "language": ""
#     }
#   },
#   "governing_law": "",
#   "notices": {
#     "customer_address": "",
#     "supplier_address": "",
#     "effective_date": ""
#   },
#   "schedules": {
#     "schedule_1_goods_specifications": "",
#     "schedule_2_mandatory_policies": ""
#   }
# }


class ContractProcessor:
    def __init__(self, llm: QueryLLM):
        self.llm = llm

    def load_document(self, filepath: str) -> Document:
        """Loads document form given filepath. uses docx type Document"""
        return Document(filepath)

    def extract_terms(self, document: Document, terms: json) -> dict:
        """
        Extract contract terms from a document using LLM or cache.
        """
        text = "\n".join([p.text for p in document.paragraphs])
        
        messages = [
                    {"role": "system", "content": f"You're an AI assistant that extracts structured information from documents and outputs it in the JSON format: {terms}"},
                    {"role": "user", "content": f"Extract the key details from the following document and format them as a JSON object:\n\n{text}"}
        ]
        response = self.llm.query_llm(messages)

        # Parse the response
        # extracted_terms = json.loads(response.choices[0].message.content[7:-4])
        
        return response
    
    def extract_terms_with_locations(self, document: Document, fields: list) -> dict:
        text = "\n".join([p.text for p in document.paragraphs]) 
        messages = [
                    {"role": "system", "content": f"You're an AI assistant document parser extracting key information from contracts. Analyze the following document and extract the specified fields along with the locations where they were found the 'start_position' must be at the start of the information sumarised by the 'value' and the 'end_position' after. The fields are: {fields}. For each 'field' in fields, return a JSON of the result in this format: {{'field'{{'value': 'value', 'start_position': start, 'end_position': end}}...}}"},
                    {"role": "user", "content": f"Extract the key details from the following document and format them as described above. do not make up any values. if you are unsure leave it like: {{'field'{{'value': '', 'start_position': '', 'end_position': ''}}...}}. Any fields you fill, you must reference their start and end locations:\n\n{text}"}
        ]
        response = self.llm.query_llm(messages)

        # Parse the response
        # extracted_terms = json.loads(response.choices[0].message.content[7:-4])
        
        return response
    
    def generate_html_highlight(self, document: Document, annotations: dict, output_path: str):
        # Generate text from document
        text = "\n".join([p.text for p in document.paragraphs])
        # Sort extracted fields by start_position
        sorted_fields = sorted(annotations.values(), key=lambda x: int(x['start_position']) if x['start_position'] else float('inf'))

        # Adjust text with HTML tags for highlights
        offset = 0
        for field in sorted_fields:
            if field['value']:  # Skip empty fields
                start = field['start_position'] + offset
                end = field['end_position'] + offset
                text = (
                    text[:start]
                    + f'<span style="background-color: yellow;">{text[start:end]}</span>'
                    + text[end:]
                )
                offset += len('<span style="background-color: yellow;"></span>')

        # Save as HTML
        with open(output_path, "w") as file:
            file.write(f"<html><body><pre>{text}</pre></body></html>")
