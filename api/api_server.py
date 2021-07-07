#Imports
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from GoogleNews import GoogleNews
from requests import get as requests_get
from re import match as regex_match
from orjson import dumps as orjson_dumps
from typing import Any

import global_vars

class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson_dumps(content)

app = FastAPI(default_response_class=ORJSONResponse)

def is_valid_date(date : str):
    return bool(regex_match(global_vars.VALID_DATE_REGEX, date))

def clean_entry(item : Any):
    cookies={'CONSENT': global_vars.CONSENT_STRING}
    try:
        item['link'] = requests_get(f"http://{item['link']}", cookies=cookies).url
    except:
        return "EXCEPTION"
    return item

def generate_news(phrases : list, gn : GoogleNews):
    for phrase in phrases:
        gn.get_news(phrase)
    ret = []
    for entry in gn.results():
        cleaned_entry = clean_entry(entry)
        if(cleaned_entry == "EXCEPTION"):
            continue
        else:
            ret.append(cleaned_entry)
    return ret

@app.get("/")
async def root():
    raise HTTPException(status_code=401, detail="Requests for root are not supported!")

@app.get("/articles/")
async def read_item(phrases : str = "",
                    lang: str = global_vars.DEFAULT_LANG,
                    start: str = global_vars.DEFAULT_START,
                    end : str = global_vars.DEFAULT_END):
    phrases = phrases.split(sep=",")
    if len(phrases) == 1 and phrases[0] == "":
        raise HTTPException(status_code=410, detail=f"Please provide at least one phrase. Instead got: {phrases}")
    if not (lang in global_vars.ISO_LANGUAGE_CODES):
        raise HTTPException(status_code=410, detail=f"Lang {lang} is invalid. Please provide a correct ISO 639-1 language code.")
    if not is_valid_date(start):
        raise HTTPException(status_code=410, detail=f"Startdate {start} is invalid. Please provide a correct date in dd/mm/rrrr format.")
    if not is_valid_date(end):
        raise HTTPException(status_code=410, detail=f"Enddate {end} is invalid. Please provide a correct date in dd/mm/rrrr format.")
    gn_object = GoogleNews(lang = lang, start = start, end = end)
    return generate_news(phrases, gn_object)
