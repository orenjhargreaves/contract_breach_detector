from docx import Document
import openai
import os
import pickle
import json

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
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def load_document(self, filepath: str) -> Document:
        return Document(filepath)

    def extract_terms(self, document: Document, terms: json) -> dict:
        # Example LLM prompt
        text = "\n".join([p.text for p in document.paragraphs])
        # prompt = f"Extract contract terms: returning the answers in the following format {extracted_terms_format} using the following text: {text}"
        # print(prompt)
        messages = [
                    {"role": "system", "content": f"You are an AI assistant that extracts structured information from documents and outputs it in the JSON format: {terms}"},
                    {"role": "user", "content": f"Extract the key details from the following document and format them as a JSON object:\n\n{text}"}
]

        # response = self.client.chat.completions.create(model=self.model, messages=messages)
        # with open('/home/oren/Documents/Python/magentic_poc/contract_breach_detector/contracts/alum_resonse.pkl', 'wb') as file:
        #     pickle.dump(response, file)
        with open('/home/oren/Documents/Python/magentic_poc/contract_breach_detector/contracts/alum_resonse.pkl', 'rb') as file:
            response = pickle.load(file)

        
        return json.loads(response.choices[0].message.content[7:-4])
        # return response