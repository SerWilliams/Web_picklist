import uvicorn
from settings import settings


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.service_host,
        port=settings.service_port,
        reload=True,
    )
