# import libraries
from rank_bm25 import BM25Okapi
from sklearn.preprocessing import MinMaxScaler as Scaler
import os, numpy as np

# initial root-dir
CURDIR = os.path.dirname(os.path.realpath(__file__))
ROOTDIR = os.path.dirname(CURDIR)

# BM25 model with multi-feature weightings
class BM25:
    def __init__(self, corpus_title:list[list], corpus_description:list[list], weights:list) -> None:
        self.model = {
            'title': BM25Okapi(corpus_title), 
            'description': BM25Okapi(corpus_description)
        }
        self.W = weights
        
    def similarity(self, query:list, normalize:bool=False) -> list:
        scores = {
            'title': self.model['title'].get_scores(query), 
            'description': self.model['description'].get_scores(query)
        }
        if normalize:
            scores['title'] = Scaler().fit_transform(np.array(scores['title']).reshape(-1, 1)).flatten()
            scores['description'] = Scaler().fit_transform(np.array(scores['description']).reshape(-1, 1)).flatten()
        
        return (self.W[0] * scores['title']) + (self.W[1] * scores['description'])