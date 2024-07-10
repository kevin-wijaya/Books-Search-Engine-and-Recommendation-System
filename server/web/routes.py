import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT) if ROOT not in sys.path else None

from fastapi import APIRouter, Request
from src.preprocessing import Preprocessing
from src.modeling import BM25
import pandas as pd

BOOKS = pd.read_pickle(os.path.join(ROOT, 'data', 'prepared_books.pkl'))
recommender = BM25(
    corpus_title=BOOKS['title_processed'].tolist(), 
    corpus_description=BOOKS['description_processed'].tolist(),
    weights=[0.7, 0.3]
)
ROUTER = APIRouter()

@ROUTER.post('/search')
async def recommendedBySearch(req: Request) -> dict:
    try:
        request = await req.json()
        
        query = request['query']
        
        print(f'{query =}')
        
        preprocessed_query = Preprocessing().fit_transform(query)
        print(f'{preprocessed_query =}')
        
        recommended_books = BOOKS.loc[:]
        recommended_books['bm25'] = recommender.similarity(preprocessed_query, normalize=True)
        recommended_books = recommended_books.sort_values(by='bm25', ascending=False)
        recommended_books = recommended_books.iloc[:12]
        print(f'table: {recommended_books.head()}', '='*50)
        return {'output': recommended_books.to_dict(orient='records')}
        
    except Exception as e: 
        print(f'[ERRO] {e}')
        
        return {'data': [], 'request': await req.json()}

@ROUTER.post('/recalculate')
async def recalculate(req: Request) -> dict:
    global recommender
    request = await req.json()
    print(recommender.W)
    recommender = BM25(
        corpus_title=BOOKS['title_processed'].tolist(), 
        corpus_description=BOOKS['description_processed'].tolist(),
        weights=[float(request['wTitle']), float(request['wDescription'])]
    )
    print(recommender.W)
    return {'status': 'oke'}

