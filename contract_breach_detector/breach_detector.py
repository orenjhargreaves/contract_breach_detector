from DB_code import DataBase


class DetectBreach:
    def __init__(self, contract_details, db: DataBase):
        self.contract_details= contract_details
        self.db = db

        self.contract_number = self.contract_details["contract_number"]
    
    def searchdb(self):
        """"searches db for contract number"""

        ERP_info = self.db.lookup_contract(self.contract_number)
        return ERP_info