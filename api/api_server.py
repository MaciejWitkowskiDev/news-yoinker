#Constants
VALID_DATE_REGEX = r"^(?:(?:31(\/)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"

#Imports
from fastapi import FastAPI, HTTPException
from datetime import date
from GoogleNews import GoogleNews
from pycountry import languages
from re import match as regex_match


app = FastAPI()

def get_language_codes():
    return [lang.iso639_1_code for lang in languages if hasattr(lang, 'iso639_1_code')]

def is_valid_date(date : str):
    return bool(regex_match(VALID_DATE_REGEX, date))


@app.get("/")
async def root():
    raise HTTPException(status_code=401, detail="Requests for root are not supported!")

@app.get("/articles/")
async def read_item(phrases : list = [],
                    lang: str = "en",
                    start: str = '01/01/2000',
                    end : str = date.today().strftime("%d/%m/%Y")):
    if len(phrases) == 0:
        raise HTTPException(status_code=410, detail="Please provide at least one phrase.")
    if lang not in get_language_codes():
        raise HTTPException(status_code=410, detail=f"Lang {lang} is invalid. Please provide a correct ISO 639-1 language code.")
    if not is_valid_date(start):
        raise HTTPException(status_code=410, detail=f"Startdate {start} is invalid. Please provide a correct date in dd/mm/rrrr format.")
    if not is_valid_date(end):
        raise HTTPException(status_code=410, detail=f"Enddate {end} is invalid. Please provide a correct date in dd/mm/rrrr format.")
