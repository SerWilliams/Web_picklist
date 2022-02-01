from typing import Optional

from fastapi import APIRouter, Form, UploadFile, File, Response,  HTTPException, status
from picklist.service.converter import Picklist as srv_pick
router = APIRouter(
    prefix='/converter',
)


@router.post('/')
async def convert_xlsx(file: Optional[UploadFile] = None):
    '''
    Загрузка таблицы xlsx\n
    Конвертация в xml\n
    Отдача picklist.xml\n
    '''
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'detail': 'File not found'}
        )
    else:
        picklist_xml = srv_pick()
        picklist_xml = picklist_xml.converter(file.file.read())
        return Response(content=picklist_xml, status_code=200, media_type="application/xml")
