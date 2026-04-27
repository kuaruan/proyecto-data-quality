from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="mvp dataops v2")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception): # Evita la visualización y ubicación de errores
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Ocurrió un error inesperado en el procesamiento de datos.",
            "hint": "Revisa los tipos de datos de tu archivo o la conexión a la base de datos."
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError): # Indica errores de composición de datos
    return JSONResponse(
        status_code=422,
        content={
            "status": "invalid_data",
            "message": "El formato de los datos no es correcto.",
            "errors": "Asegúrate de seguir el esquema requerido."
        }
    )


@app.get("/")
def read_root():
    return {"message": "API de Data Quality operativa"}