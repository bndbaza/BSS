from typing import List
from fastapi import APIRouter, File, UploadFile, Form
import shutil
from datetime import date
from fastapi.responses import FileResponse
from models import Entry

router = APIRouter(prefix="/entry",tags=["entry"])


@router.get('', response_model=List[Entry])
async def get_entry():
    entry = await Entry.objects.all()
    return entry

@router.get('/{id}', response_model=Entry)
async def get_entry(id):
    entry = await Entry.objects.get(id = id)
    return entry

@router.post('')
async def post_entry(entry: Entry):
    await entry.save()
    return entry

@router.post('/file',response_model=Entry)
async def create(
    file: UploadFile = File(...),
    Organ: str = Form(...),
    Address: str = Form(...),
    Content: str = Form(...),
    Sender: str = Form(...),
    Wey: str = Form(...),
):  
    regN = {'ООО Байкальский завод металлоконструкций': 3, 'ООО Байкалстальстрой 2015': 2, 'ООО Байкалстальстрой': 1}
    tmp = await Entry.objects.filter(Entry.Date % date.today().strftime("%Y-%m")).filter(Organ=Organ).max('id')
    if tmp:
        tmp = await Entry.objects.get(id=tmp)
        name_id = int(str(tmp.RegNumber).split('/')[-1]) + 1
    else:
        name_id = '1'
    RegNumber = (f'{regN[Organ]}-{date.today().strftime("%y/%m")}/{name_id}')
    file_name = 'media/Entry/' + (f'{RegNumber}').replace('/','_') + '.' + (file.filename).split('.')[-1]
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return await Entry.objects.create(
        RegNumber=RegNumber,
        Date=date.today(),
        Organ=Organ,
        Address=Address,
        Content=Content,
        Sender=Sender,
        Wey=Wey,
        Files=file_name,
        )

@router.get('/file/{id}')
async def files(id):
    files = await Entry.objects.get(id=id)
    return FileResponse(files.Files)