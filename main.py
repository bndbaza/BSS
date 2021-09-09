from typing import List
from fastapi import FastAPI, File, UploadFile,Form
from fastapi.responses import FileResponse
from models import *
from db import  database
import shutil

app = FastAPI()
app.state.database = database

@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.post('/entry')
async def post_entry(entry: Entry):
    await entry.save()
    return entry

@app.get('/entry', response_model=List[Entry])
async def get_entry():
    entry = await Entry.objects.all()
    return entry

@app.get('/entry/{id}', response_model=Entry)
async def get_entry(id):
    entry = await Entry.objects.get(id = id)
    return entry


@app.post('/entry/file')
async def create(
    file: UploadFile = File(...),
    RegNumber: str = Form(...),
    Date: datetime.date = Form(...),
    Organ: str = Form(...),
    Address: str = Form(...),
    Content: str = Form(...),
    Sender: str = Form(...),
    Wey: str = Form(...),
):
    file_name = f'media/{file.filename}'
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return await Entry.objects.create(
        RegNumber=RegNumber,
        Date=Date,
        Organ=Organ,
        Address=Address,
        Content=Content,
        Sender=Sender,
        Wey=Wey,
        Files=file_name
        )


@app.get('/{id}')
async def files(id):
    files = await Entry.objects.get(id=id)
    return FileResponse(files.Files)