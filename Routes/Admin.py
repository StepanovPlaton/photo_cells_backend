from fastapi import APIRouter, HTTPException

from Database.Database import *
from Models.Admin import CheckToken, EditInfo
from Utils.Hasher import HasherClass
from Models.api import *
from Models.Images import *

router = APIRouter()

HasherObject = HasherClass()
database = DatabaseClass()


@router.post('/admin/token', status_code=200, tags=["Admin"])
async def check_token(body: CheckToken):
    try:
        hashed_password = await database.get_password()
        try:
            token_correct = HasherObject.CheckToken(body.token, hashed_password)
        except Exception: raise HTTPException(status_code=401)
        if token_correct:
            return
        else:
            raise HTTPException(status_code=401)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')


@router.put('/about', status_code=200, tags=["Admin"])
async def edit_info(user: NeedToken, info: EditInfo):
    try:
        password = await database.get_password()
        hash = str(password)
        if HasherObject.CheckToken(user.token, hash):
            await database.edit_info(info.info)
        else:
            raise HTTPException(status_code=403, detail='Bad Token')
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')


@router.get('/about', status_code=200, tags=["Admin"])
async def AdminInfo():
    try:
        return await database.get_info()
    except DatabaseError:
        return HTTPException(status_code=500, detail='Database Error')


@router.post('/admin/auth', response_model=SuccessAuthorizationResponse, tags=["Admin"])
async def authorization(password: Authorization):
    try:
        hashed_password = await database.get_password()
        hash = str(hashed_password)
        if HasherObject.CheckPassword(hash, password.password):
            return {
                'token': HasherObject.GetToken(hash)
            }
        else:
            raise HTTPException(
                status_code=401,
                detail='Wrong Password'
            )
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')



