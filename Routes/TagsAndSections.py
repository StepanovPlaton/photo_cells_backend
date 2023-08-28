from fastapi import APIRouter, HTTPException
from Database.Database import *
from Models.Images import *
from Models.api import *
from Utils.Hasher import HasherClass

router = APIRouter()

HasherObject = HasherClass()
database = DatabaseClass()

# === /TAGS ===
@router.get('/tags', tags=["Tags"])
async def get_Tags():
    try:
        return await database.get_tags()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.post('/tags', tags=["Tags"])
async def create_tag(tag_name: str, user: NeedToken):
    try:
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if (not authorized): raise HTTPException(status_code=401, detail='Not Authorized')
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    try:
        return {"tagId": await database.create_tag(tag_name) }
    except DatabaseError:
        raise HTTPException(status_code=200, detail='OK')

@router.put('/tags/{tagId}', tags=["Tags"])
async def edit_tag_name(tagId: int, edited_name: str, user: NeedToken):
    try:
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if (not authorized): raise HTTPException(status_code=401, detail='Not Authorized')
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    try:
        await database.edit_tag_name(tagId, edited_name)
    except DatabaseError:
        raise HTTPException(status_code=200, detail='OK')

@router.delete('/tags/{tagId}', tags=["Tags"])
async def delete_tag(tagId: int, user: NeedToken):
    try:
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if (not authorized): raise HTTPException(status_code=401, detail='Not Authorized')
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    try:
        await database.delete_tag(tagId)
    except DatabaseError:
        raise HTTPException(status_code=200, detail='OK')

# === /IMAGES ===
@router.post('/images/{imageId}/tags/{tagId}', tags=["Tags", "Images"])
async def add_tag_to_image(imageId: int, tagId: int, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        await database.add_tag_to_image(imageId, tagId)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.delete('/images/{imageId}/tags/{tagId}', tags=["Tags", "Images"])
async def delete_tag_from_image(imageId: int, tagId: int, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        await database.delete_tag_from_image(imageId, tagId)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.put('/images/{imageId}', tags=["Images"])
async def change_image_priority(imageId: int, priority: int, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        await database.change_image_priority(imageId, priority)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

# === /SECTIONS ===
@router.get('/sections', tags=["Sections"])
async def get_Sections():
    try:
        return await database.get_sections()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.put('/sections/{sectionId}', tags=["Sections"])
async def change_section(sectionId: int, edited_name: str, description: str, cover: int, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        return await database.change_section(sectionId, edited_name, description, cover)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')


@router.post('/sections/{sectionId}/tags/{tagId}', tags=["Tags", "Sections"])
async def add_tag_to_section(sectionId: int, tagId: int, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        await database.add_tag_to_section(sectionId, tagId)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')


@router.delete('/sections/{sectionId}/tags/{tagId}', tags=["Tags", "Sections"])
async def delete_tag_from_section(sectionId: int, tagId: int, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        await database.delete_tag_from_section(sectionId, tagId)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')


@router.post('/sections', status_code=200, tags=["Sections"])
async def create_section(section: str, description: str, cover: int, user: NeedToken):
    try:
        hashed_password = await database.get_password()
        hash = str(hashed_password)
        if HasherObject.CheckToken(user.token, hash):
            return {"sectionId": await database.create_section(section, description, cover)}
        else:
            raise HTTPException(status_code=401, detail='Bad Token')
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')


@router.delete('/sections/{SectionId}', status_code=200, tags=["Sections"])
async def delete_section(SectionId: int, user: NeedToken):
    try:
        hashed_password = await database.get_password()
        hash = str(hashed_password)
        if HasherObject.CheckToken(user.token, hash):
            try:
                await database.delete_section(SectionId)
            except:
                raise HTTPException(status_code=404, detail='Section not Found')
        else:
            raise HTTPException(status_code=401, detail='Bad Token')
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

# === /FOLDERS ===
@router.get('/folders', tags=["Folders"])
async def get_folders():
    try:
        return await database.get_folders()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.post('/folders', status_code=200, tags=["Folders"])
async def create_folder(folder: str, user: NeedToken):
    try:
        hashed_password = await database.get_password()
        hash = str(hashed_password)
        if HasherObject.CheckToken(user.token, hash):
            return { "folderId": await database.create_folder(folder) }
        else:
            raise HTTPException(status_code=401, detail='Bad Token')
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.delete('/folders/{folderId}', status_code=200, tags=["Folders"])
async def delete_folder(folderId: int, user: NeedToken):
    try:
        hashed_password = await database.get_password()
        hash = str(hashed_password)
        if HasherObject.CheckToken(user.token, hash):
            try:
                await database.delete_folder(folderId)
            except:
                raise HTTPException(status_code=404, detail='Section not Found')
        else:
            raise HTTPException(status_code=401, detail='Bad Token')
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.post('/folders/{folderId}/sections/{sectionId}', tags=["Folders", "Sections"])
async def add_section_to_folder(folderId: int, sectionId: int, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        await database.add_section_to_folder(folderId, sectionId)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.delete('/folders/{folderId}/sections/{sectionId}', tags=["Folders", "Sections"])
async def delete_section_from_folder(folderId: int, sectionId: int, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        await database.delete_section_from_folder(folderId, sectionId)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')

@router.put('/folders/{folderId}', tags=["Folders"])
async def change_folder_name(folderId: int, edited_name: str, user: NeedToken):
    try: 
        authorized = HasherObject.CheckToken(user.token, await database.get_password())
        if(not authorized): raise Exception()
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')
    except: raise HTTPException(status_code=401)
    try:
        await database.change_folder_name(folderId, edited_name)
    except DatabaseError:
        raise HTTPException(status_code=500, detail='Database Error')