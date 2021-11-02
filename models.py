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

class Output(ormar.Model):
    class Meta:
        tablename: str = "Output"
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



class Contract(ormar.Model):
    class Meta:
        tablename: str = "Contract"
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    NumCont: str = ormar.String(max_length=500)
    Date: datetime.date = ormar.Date()
    We: str = ormar.String(max_length=500)
    They: str = ormar.String(max_length=500)
    View: str = ormar.String(max_length=500)
    Thing: str = ormar.String(max_length=500)
    Files: str = ormar.String(max_length=500)

class User(ormar.Model):
    class Meta:
        tablename: str = "Users"
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    ip: str = ormar.String(max_length=20)
    user_name: str = ormar.String(max_length=100)