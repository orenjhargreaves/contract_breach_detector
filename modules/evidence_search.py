
from .query_llm import QueryLLM
from docx import Document
from rapidfuzz import process, fuzz

class EvidenceSearch:
    """
    Will search for evidence within a document
    """

    def __init__(self, llm: QueryLLM):
        """initialises Evidence Search class
        
        Args:
            llm (QueryLLM): An instance of the LLM interface for analysis.
            """
        
        self.llm = llm
    
    def find_exact_text(self, text: str, document: Document):
        """
        when passed text that is believed to have been evidenced from a document, it will return the exact text form within the document.
        Args:
            text (str): the text to find in document
            document (Document): the document within to search
        """
        document_text = "\n".join([p.text for p in document.paragraphs])

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistent that when passed in a text string you will search the given"
                    "document and return the exact wording from the document. include required context"
                    "around the specific text, provided it forms a continuous string exactly as found in the document"
                    "in the documentThe input from the user will come in the form:"
                    "Document <document text>"
                    "text to evidence: <text>"
                    "Output in the JSON form {'evidence': <exact wording>}"
                    ""
                    "Document: 'This is a test contract. specific piece of information to be returned: password123. Rest of the test contract'"
                    "text to evidence: 'specific piece of information: password123'"
                    "{'evidence': 'specific piece of information to be returned: password123'"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Document: {document_text}"
                    f"text to evidence: {text}"
                    "{'evidence': "
                ),
            },
        ]
        #removed from content: If you can not find any" "relavent text return {'evidence': 'None'}.

        # Query the LLM
        response = self.llm.query_llm(messages)
        return response
    
    def find_best_fuzzy_match(self, text:str, document: Document, threshold=80):
        """
        when given text and a document it will find the location of the best match
        Args:
            text (str): the text to find in the document
            document (Document): the document in which to find text
        """
        document_text = "\n".join([p.text for p in document.paragraphs])
        # Use rapidfuzz to calculate similarity score
        score = fuzz.token_set_ratio(text, document_text)
        
        # Check if score meets the threshold
        if score >= threshold:
            # Locate the start and end indexes of the best match
            start_index = document_text.find(text)
            if start_index != -1:
                end_index = start_index + len(text)
            return score, start_index, end_index
        else:
            return None