from fastapi import FastAPI
from pydantic import BaseModel
import verify
from datetime import date

class blabla(BaseModel):
    day: str  
    session: int 
    className: str

app = FastAPI()


@app.post('/verify-booking')
async def verifyBooking(req: blabla):
    date = req.day
    session = req.session
    className = req.className

    result = verify.alreadyBooked(className, date, session)
    return result
