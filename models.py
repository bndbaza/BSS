import ormar
import datetime
from db import database, metadata

class Entry(ormar.Model):
    class Meta:
        tablename: str = "Entry"
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    RegNumber: str = ormar.String(max_length=500)
    Date: datetime.date = ormar.Date()
    Organ: str = ormar.String(max_length=500)
    Address: str = ormar.String(max_length=500)
    Content: str = ormar.String(max_length=500)
    Sender: str = ormar.String(max_length=500)
    Wey: str = ormar.String(max_length=500)
    Files: str = ormar.String(max_length=500)