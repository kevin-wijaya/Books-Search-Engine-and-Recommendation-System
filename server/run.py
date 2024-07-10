from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web.routes import ROUTER
import sys

origins = [
    '*'
]   

print(f'origins: {origins}')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

print('Server started successfully')

app.include_router(ROUTER, prefix="/api-v1")

sys.stdout.flush()