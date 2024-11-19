from DB_code import DataBase
from query_llm import QueryLLM
import json

class DetectBreach:
    def __init__(self, contract, db: DataBase, llm: QueryLLM):
        self.contract= contract
        self.db = db
        self.llm = llm

        self.contract_number = self.contract["info"]["contract_number"]
    
    def searchdb(self):
        """"searches db for contract number"""

        ERP_info = self.db.lookup_contract(self.contract_number)
        return ERP_info
    
    def get_comparisons(self, ERP_info) -> list:
        """for each of the details in the contract, check it against the DB"""
        contract_vs_actuals = []
        for k,v in self.contract["details"].items():
            ERP_value = ERP_info[k][0]
            contract_vs_actuals.append(f"The contract states that the value for {k} should be {v}. the delivered value was {ERP_value}")
        return contract_vs_actuals
    
    def analyse_comparisons(self, comparisons: list):
        """
        Look up whether any of the contract details are breached
        """
        text = "\n".join(comparisons)
        
        messages = [
                    {"role": "system", "content": f"You're an AI assistant that will be given a list of contractual obligations and delivered values. it is your job to return if any of the obligations have been breached. If a delivery_date is early of a greater quantity it delivered than in the contract this is not a breach. You will output a JSON of the form {{'breached': <True/False>, 'breached_description': <description of the breach>}} the description of the breach should refer to the expected value in the contract and the delivered value. If there is a missing value treat the contact as breached but state that human clairification is required due to a missing value and report this last."},
                    {"role": "user", "content": f"inspect the following contract and delivered values separated by new lines: {comparisons} output your response following the JSON schema: {{'breached': <True/False>, 'breached_description': <description of the breach>}}"}
        ]
        response = self.llm.query_llm(messages)
        # print(response) # for debugging

        # Parse the response
        # extracted_terms = json.loads(response.choices[0].message.content)
        
        return response
