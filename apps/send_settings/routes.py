from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from starlette.responses import JSONResponse

from apps.send_settings.querys import get_send_settings_query, add_settings_for_user_query, delete_settings_query, \
    update_settings_query, get_list_send_settings_query
from apps.send_settings.schemas import SendSettingsSchema, SendSettingsUpdateSchema
from apps.users.querys import get_user_query
from database.async_connect_postgres import Session, get_session

router = APIRouter(prefix='/settings_for_users')


@router.get('/{user_id}', response_model=List[SendSettingsSchema])
async def get_list_user_settings(user_id: int, db: Session = Depends(get_session)):
    query = text(get_list_send_settings_query).bindparams(user_id=user_id)
    cursor = await db.execute(query)
    user_settings = cursor.fetchall()
    if not user_settings:
        raise HTTPException(status_code=404, detail=f"Setting for user with id = {user_id} not found")
    return user_settings


@router.get('/{user_id}/{type_event}', response_model=SendSettingsSchema)
async def get_detail_user_settings(user_id: int, type_event: str, db: Session = Depends(get_session)):
    query = text(get_send_settings_query).bindparams(user_id=user_id, type_event=type_event)
    cursor = await db.execute(query)
    user_settings = cursor.fetchone()
    if not user_settings:
        raise HTTPException(status_code=404, detail=f"Setting for user with id = {user_id} and {type_event} not found")
    return user_settings


@router.post('/add')
async def add_settings_for_user(user_settings: SendSettingsSchema, db: Session = Depends(get_session)):
    query = text(get_user_query).bindparams(user_id=user_settings.user_id)
    cursor = await db.execute(query)
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404,
                            detail=f"User with id={user_settings.user_id} not found")
    query = text(get_send_settings_query).bindparams(user_id=user_settings.user_id, type_event=user_settings.type_event)
    cursor = await db.execute(query)
    user = cursor.fetchone()
    if user:
        raise HTTPException(status_code=404,
                            detail=f"User with id={user_settings.user_id} and {user_settings.type_event} already exists")
    query = text(add_settings_for_user_query).bindparams(**user_settings.dict())
    await db.execute(query)
    await db.commit()
    return JSONResponse(status_code=201, content={'msg': 'settings for users was created'})


@router.delete('/{user_id}/{type_event}', response_model=SendSettingsSchema)
async def delete_settings_for_user(user_id: int, type_event: str, db: Session = Depends(get_session)):
    query = text(get_send_settings_query).bindparams(user_id=user_id, type_event=type_event)
    cursor = await db.execute(query)
    user_settings = cursor.fetchone()
    if not user_settings:
        raise HTTPException(status_code=404, detail=f"Settings for user {user_id} not found")
    query = text(delete_settings_query).bindparams(user_id=user_id, type_event=type_event)
    await db.execute(query)
    await db.commit()
    return JSONResponse(status_code=200, content={'msg': f'settings for user with id = {user_id} was deleted'})


@router.put('/{user_id}/{type_event}', response_model=SendSettingsUpdateSchema)
async def update_settings_for_user(user_id: int, type_event: str, user_settings: SendSettingsUpdateSchema,
                                   db: Session = Depends(get_session)):
    query = text(get_send_settings_query).bindparams(user_id=user_id, type_event=type_event)
    cursor = await db.execute(query)
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail=f"Settings for user {user_id} not found")
    query = text(update_settings_query).bindparams(**user_settings.dict(), user_id=user_id, type_event=type_event)
    await db.execute(query)
    await db.commit()
    return JSONResponse(status_code=200, content={'msg': f'Settings for user with id = {user_id} was updated'})
