from DB_code import DataBase


class DetectBreach:
    def __init__(self, contract, db: DataBase):
        self.contract= contract
        self.db = db

        self.contract_number = self.contract["info"]["contract_number"]
    
    def searchdb(self):
        """"searches db for contract number"""

        ERP_info = self.db.lookup_contract(self.contract_number)
        return ERP_info
    
    def compare_details(self, ERP_info):
        """for each of the details in the contract, check it against the DB"""

        for k,v in self.contract["details"].items():
            ERP_value = ERP_info[k][0]
            print(f"The contract states that the value for {k} should be {v}. the delivered value was {ERP_value}")