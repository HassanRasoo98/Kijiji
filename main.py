# main.py
from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get('/')
def home():
    return "welcome to kijiji bot"



if __name__ == '__main__':
    uvicorn.run(app, port=8000)