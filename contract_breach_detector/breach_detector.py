from DB_code import DataBase
from query_llm import QueryLLM
import json

class DetectBreach:
    """
    DetectBreach is a class for detecting contract breaches by comparing 
    contractual obligations with actual delivered values stored in a database.

    Attributes:
        contract (dict): The contract details including info and expected values.
        db (DataBase): The database instance to query for actual delivered values.
        llm (QueryLLM): The LLM interface for analyzing comparisons and breaches.
    """

    def __init__(self, contract: dict, db: DataBase, llm: QueryLLM):
        """
        Initializes the DetectBreach class.

        Args:
            contract (dict): The contract details to evaluate.
            db (DataBase): A database instance to query for delivered values.
            llm (QueryLLM): An instance of the LLM interface for analysis.
        """
        self.contract = contract
        self.db = db
        self.llm = llm
        self.contract_number = self.contract["info"]["contract_number"]

    def searchdb(self) -> dict:
        """
        Searches the database for information about the contract.

        Returns:
            dict: The ERP information retrieved from the database.
        """
        return self.db.lookup_contract(self.contract_number)

    def get_comparisons(self, ERP_info: dict) -> list:
        """
        Compares the contract details against the values retrieved from the database.

        Args:
            ERP_info (dict): The ERP information retrieved from the database.

        Returns:
            list: A list of strings describing the comparisons between 
                  contract values and delivered values.
        """
        contract_vs_actuals = []
        for key, expected_value in self.contract["details"].items():
            actual_value = ERP_info.get(key, [""])[0]  # Safely handle missing keys
            comparison = (
                f"The contract states that the value for {key} should be {expected_value}. "
                f"The delivered value was {actual_value}."
            )
            contract_vs_actuals.append(comparison)
        return contract_vs_actuals

    def analyse_comparisons(self, comparisons: list) -> dict:
        """
        Analyzes comparisons to detect contract breaches using an LLM.

        Args:
            comparisons (list): A list of comparisons between contract values and delivered values.

        Returns:
            dict: A JSON object describing whether the contract is breached 
                  and the reasons for the breach.
        """
        text = "\n".join(comparisons)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant tasked with determining whether contractual obligations "
                    "have been breached based on provided comparisons of expected and delivered values. "
                    "If a delivery_date value is early or a greater quantity is delivered than in the contract, "
                    "this is not a breach. If a value is missing, treat it as a breach and state that "
                    "human clarification is required. Your response must be in JSON format as follows: "
                    "{'breached': <True/False>, 'breached_description': <description of the breach>}"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Inspect the following contract and delivered values separated by new lines: {text} "
                    "Output your response following the JSON schema: "
                    "{'breached': <True/False>, 'breached_description': <description of the breach>}"
                ),
            },
        ]

        # Query the LLM
        response = self.llm.query_llm(messages)

        # For debugging purposes, uncomment the following line:
        # print("LLM Response:", response)

        # Assuming the response is already in JSON format; parse if necessary
        # Uncomment the following line if the response needs to be parsed:
        # response = json.loads(response.choices[0].message.content)

        return response
