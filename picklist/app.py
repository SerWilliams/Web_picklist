from fastapi import FastAPI

from api import router


tags_metadata = [
    {
        'name': 'Converter Picklist',
    },
]

app = FastAPI(
    title='PicklistCreator',
    description='Сервис конвертирования таблицы xlsx в файл picklist.xml ',
    version='1.0.0',
    openapi_tags=tags_metadata,
)


app.include_router(router)

