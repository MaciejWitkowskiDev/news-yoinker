from fastapi import FastAPI, HTTPException
from datetime import date

app = FastAPI()

@app.get("/")
async def root():
    raise HTTPException(status_code=401, detail="Requests for root are not supported!")

@app.get("/articles/")
async def read_item(phrases : list = [],
                    lang: str = "en",
                    start: str = '01/01/2000',
                    end : str = date.today().strftime("%d/%m/%Y")):
    return 0