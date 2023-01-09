
from fastapi.responses import JSONResponse


def customResponse(status:int, msg:str , success=True, data=None,):

    return JSONResponse(
        status_code=status,
        content={
        "status":status,
        "msg": msg,
        "success": success,
        "data": data if data != None else None
        }
    )



