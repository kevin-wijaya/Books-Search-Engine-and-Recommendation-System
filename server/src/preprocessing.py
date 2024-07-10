# import libraries
from nltk.tokenize import word_tokenize
import re, nltk

# download punkt package
nltk.download('punkt', quiet=True)

# preprocessing pipeline
class Preprocessing:
    def __init__(self) -> None:
        self.pipeline = [
            self.case_folding, 
            self.cleaning, 
            self.tokenizing
        ]
    
    def case_folding(self, text:str) -> str:
        return str(text).lower()

    def cleaning(self, text:str) -> str:
        text = text.replace('\n', ' ')
        text = text.strip(' ')
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def tokenizing(self, text:str) -> list:
        return word_tokenize(text)

    def fit_transform(self, text:str) -> list:
        for fn in self.pipeline:
            text = fn(text)
        return text