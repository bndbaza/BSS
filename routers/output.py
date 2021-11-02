from typing import List
from fastapi import APIRouter, File, UploadFile, Form, Request
import shutil
from datetime import date
from fastapi.responses import FileResponse
from models import Output, User


router = APIRouter(prefix="/output",tags=["output"])

@router.get('', response_model=List[Output])
async def get_output():
    output = await Output.objects.all()
    return output


@router.get('/{id}', response_model=Output)
async def get_output(id):
    output = await Output.objects.get(id = id)
    return output

@router.post('')
async def post_output(output: Output):
    await output.save()
    return output

@router.post('/file',response_model=Output)
async def create(request: Request,
    file: UploadFile = File(...),
    Organ: str = Form(...),
    Address: str = Form(...),
    Content: str = Form(...),
    Wey: str = Form(...),
):  
    regN = {'ООО Байкальский завод металлоконструкций': 3, 'ООО Байкалстальстрой 2015': 2, 'ООО Байкалстальстрой': 1}
    tmp = await Output.objects.filter(Output.Date % date.today().strftime("%Y-%m")).filter(Organ=Organ).max('id')
    if tmp:
        tmp = await Output.objects.get(id=tmp)
        name_id = int(str(tmp.RegNumber).split('/')[-1]) + 1
    else:
        name_id = '1'
    RegNumber = (f'{regN[Organ]}-{date.today().strftime("%y/%m")}/{name_id}')
    file_name = 'media/Output/' + (f'{RegNumber}').replace('/','_') + '.' + (file.filename).split('.')[-1]
    ip = await User.objects.get(ip=request.client.host)
    sender = ip.user_name
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return await Output.objects.create(
        RegNumber=RegNumber,
        Date=date.today(),
        Organ=Organ,
        Address=Address,
        Content=Content,
        Sender= sender,
        Wey=Wey,
        Files=file_name,
        )

@router.put('/files/put/{id}', response_model=Output)
async def update(id: int, file: UploadFile =File(...)):
    track = await Output.objects.get(id=id)
    file_name = track.RegNumber
    file_name = 'media/Output/' + (f'{file_name}').replace('/','_') + '.' + (file.filename).split('.')[-1]
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    await track.update(Files=file_name)

@router.get('/file/{id}')
async def files(id):
    files = await Output.objects.get(id=id)
    return FileResponse(files.Files)