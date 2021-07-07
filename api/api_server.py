from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    raise HTTPException(status_code=401, detail="Requests for root are not supported!")
