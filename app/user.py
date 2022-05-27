from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Exp: async",
    description= "Experimento con fastapi, sqlalchemy y asyncio.",
    version="0.0.1")

#Funcion para responder cuando el usuario ingrese una ruta invalida
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse({
        "error": True,
        "message": "Ruta invalida.",
        "res": None,
        }
    )

#Funcion para responder cuando faltan campos
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "error": True, 
            "message": "Inexistencia de campos.", 
            "res": None
        }),
    )

#Solucion CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port="8000")

#>> conexion a client de Routes
#app.include_router(routes)