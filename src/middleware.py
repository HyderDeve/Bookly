from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import time
import logging

logger = logging.getLogger('uvicorn.access')
logger.disabled = True   #Disable the default uvicorn logger


def register_middleware(app: FastAPI):
    
    
    @app.middleware('http')
    async def custom_logging(request : Request, call_next):
        
        start_time = time.time()

        response = await call_next(request)

        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - Status Code: {response.status_code} - Completed after {processing_time}s"

        print(message)
        
        return response
    
    
#------------------- We Have Implemented This Using Dependency Injection -----------------#

    # @app.middleware('http')
    # async def authorization_middleware(request : Request, call_next):
        
    #     if not 'Authorization' in request.headers:
    #         return JSONResponse(
    #             content = {'message' : 'Not Authenticated',
    #                        'Resolution' : 'Provide Valid Credentials'},
    #             status_code = status.HTTP_401_UNAUTHORIZED
    #         )
        
    #     response = await call_next(request)

    #     return response

#------------------- We Have Implemented This Using Dependency Injection -----------------#


