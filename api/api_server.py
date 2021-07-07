from fastapi import FastAPI, HTTPException
from datetime import date
from GoogleNews import GoogleNews
from pycountry import languages

app = FastAPI()

def get_language_codes():
    return [lang.iso639_1_code for lang in languages if hasattr(lang, 'iso639_1_code')]

def check_valid_date():
    pass


@app.get("/")
async def root():
    raise HTTPException(status_code=401, detail="Requests for root are not supported!")

@app.get("/articles/")
async def read_item(phrases : list = [],
                    lang: str = "en",
                    start: str = '01/01/2000',
                    end : str = date.today().strftime("%d/%m/%Y")):
    
    gn_object = GoogleNews()
    if lang not in get_language_codes():
        raise HTTPException(status_code=410, detail=f"Lang {lang} is invalid. Please provide a correct ISO 639-1 language code.")