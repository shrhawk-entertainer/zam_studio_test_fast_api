import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from apis.routing import setup_routing
from common.constants import DEBUG_MODE

app = FastAPI()
setup_routing(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = {"errors": {}}
    for error in exc.errors():
        errors["errors"][error['loc'][-1]] = error['msg']
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(errors),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=DEBUG_MODE)
