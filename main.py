from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date

app = FastAPI(title="Easter Calculator API")

class YearRequest(BaseModel):
    # Ustalamy logiczne granice dla roku (np. kalendarz gregoriański od 1583 roku)
    year: int = Field(..., ge=1583, le=4000)

@app.post("/easter")
def calculate_easter_endpoint(data: YearRequest):
    Y = data.year
    
    # Implementacja algorytmu Meeusa/Jonesa/Butchera
    a = Y % 19
    b = Y // 100
    c = Y % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    
    # Generujemy pełną datę obiektu dla backendu
    easter_date = date(Y, month, day)
    
    return {
        "year": Y,
        "easter_sunday": easter_date.isoformat(),
        "month_name": "March" if month == 3 else "April"
    }
