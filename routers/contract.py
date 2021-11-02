import datetime
from typing import List
from fastapi import APIRouter, File, UploadFile, Form, Request
from datetime import date
import shutil
from fastapi.responses import FileResponse
from sqlalchemy.sql.elements import Null
from models import Contract, User

router = APIRouter(prefix="/contract",tags=["contract"])


@router.get('', response_model=List[Contract])
async def get_contract():
    contract = await Contract.objects.all()
    return contract

@router.get('/{id}', response_model=Contract)
async def get_contract(id):
    contract = await Contract.objects.get(id = id)
    return contract

@router.post('')
async def post_contract(contract: Contract):
    await contract.save()
    return contract

@router.post('/file',response_model=Contract)
async def create(request: Request,
    file: UploadFile = File(...),
    We: str = Form(...),
    NumCont: str = Form(...),
    They: str = Form(...),
    View: str = Form(...),
    Thing: str = Form(...),
    Date: str = Form(...),
):  
    Date = datetime.date(int(Date.split('.')[2]),int(Date.split('.')[1]),int(Date.split('.')[0]))
    regN = {'ООО Байкальский завод металлоконструкций': 'БЗМ', 'ООО Байкалстальстрой 2015': 'БСС'}
    regView = {'Аренда': 'А','Купли-продажи': 'КП','Хранения': 'Х','Подряда': 'Пд','Изготовление металлоконструкций': 'ИМ','Поставки': 'Пс','Оказания услуг': 'ОУ'}
    if (NumCont == 'undefined'):
        tmp = await Contract.objects.filter(Contract.Date % Date.strftime("%Y")).filter(We=We).count()
        NumCont = (f'{regN[We]}-{Date.today().strftime("%y")}/{tmp + 1}{regView[View]}')
    file_name = 'media/Contract/' + (f'{NumCont}').replace('/','_') + '.' + (file.filename).split('.')[-1]
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return await Contract.objects.create(
        Date=Date,
        We=We,
        They=They,
        View=View,
        Thing=Thing,
        Files=file_name,
        NumCont=NumCont,
        )

@router.get('/file/{id}')
async def files(id):
    files = await Contract.objects.get(id=id)
    return FileResponse(files.Files)