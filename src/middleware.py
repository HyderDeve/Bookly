from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging

logger = logging.getLogger('uvicorn.access')
logger.disabled = True   #Disable the default uvicorn logger


def register_middleware(app: FastAPI):
    
    
    @app.middleware('http')
    async def custom_logging(request : Request, call_next):
        
        start_time = time.time()

        print('Before Processing', start_time)

        response = await call_next(request)

        processing_time = time.time() - start_time

        print('After Processing', processing_time)
        
        return response


