#Imports
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import date
from GoogleNews import GoogleNews
from random import randint
from requests import get as requests_get
from re import match as regex_match
from orjson import dumps as orjson_dumps
from typing import Any

#Constants
DATE_V = "%Y%m%d"
CONSENT_STRING = f"YES+cb.{date.today().strftime(DATE_V)}-17-p0.en-GB+FX+{randint(100, 999)}"
VALID_DATE_REGEX = r"^(?:(?:31(\/)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
LANGUAGES = [('vi', 'Vietnamese'), ('ku', 'Kurdish'), ('ne', 'Nepali'), ('te', 'Telugu'), ('ru', 'Russian'), ('ar', 'Arabic'), ('ta', 'Tamil'), ('lv', 'Latvian'), ('el', 'Greek'), ('az', 'Azerbaijani'), ('hy', 'Armenian'), ('pa', 'Panjabi; Punjabi'), ('fr', 'French'), ('cy', 'Welsh'), ('bo', 'Tibetan'), ('ms', 'Malay'), ('sl', 'Slovenian'), ('bs', 'Bosnian'), ('tl', 'Tagalog'), ('tr', 'Turkish'), ('eu', 'Basque'), ('lt', 'Lithuanian'), ('en', 'English'), ('fi', 'Finnish'), ('sq', 'Albanian'), ('cs', 'Czech'), ('cv', 'Chuvash'), ('de', 'German'), ('Ga', 'Georgian'), ('ga', 'Irish'), ('hu', 'Hungarian'), ('rm', 'Romansh'), ('no', 'Norwegian'), ('th', 'Thai'), ('be', 'Belarusian'), ('fa', 'Persian'), ('uz', 'Uzbek'), ('sr', 'Serbian'), ('sw', 'Swahili'), ('zh', 'Chinese'), ('pl', 'Polish'), ('hr', 'Croatian'), ('pt', 'Portuguese'), ('af', 'Afrikaans'), ('ko', 'Korean'), ('nl', 'Dutch; Flemish'), ('it', 'Italian'), ('sv', 'Swedish'), ('my', 'Burmese'), ('is', 'Icelandic'), ('mk', 'Macedonian'), ('sk', 'Slovak'), ('es', 'Spanish'), ('ja', 'Japanese'), ('ro', 'Romanian'), ('bg', 'Bulgarian'), ('he', 'Hebrew'), ('eo', 'Esperanto'), ('uk', 'Ukrainian'), ('id', 'Indonesian'), ('ka', 'Georgian'), ('hi', 'Hindi'), ('mr', 'Marathi'), ('et', 'Estonian'), ('da', 'Danish'), ('ca', 'Catalan; Valencian'), ('mn', 'Mongolian')]
ISO_LANGUAGE_CODES = [item[0] for item in LANGUAGES]

class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson_dumps(content)

app = FastAPI(default_response_class=ORJSONResponse)

def is_valid_date(date : str):
    return bool(regex_match(VALID_DATE_REGEX, date))

def clean_entry(item : Any):
    cookies={'CONSENT': CONSENT_STRING}
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
                    lang: str = "en",
                    start: str = '01/01/2000',
                    end : str = date.today().strftime("%d/%m/%Y")):
    phrases = phrases.split(sep=",")
    if len(phrases) == 1 and phrases[0] == "":
        raise HTTPException(status_code=410, detail=f"Please provide at least one phrase. Instead got: {phrases}")
    if not (lang in ISO_LANGUAGE_CODES):
        raise HTTPException(status_code=410, detail=f"Lang {lang} is invalid. Please provide a correct ISO 639-1 language code.")
    if not is_valid_date(start):
        raise HTTPException(status_code=410, detail=f"Startdate {start} is invalid. Please provide a correct date in dd/mm/rrrr format.")
    if not is_valid_date(end):
        raise HTTPException(status_code=410, detail=f"Enddate {end} is invalid. Please provide a correct date in dd/mm/rrrr format.")
    gn_object = GoogleNews(lang = lang, start = start, end = end)
    return generate_news(phrases, gn_object)
