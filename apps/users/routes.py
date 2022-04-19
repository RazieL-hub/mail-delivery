from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from starlette.responses import JSONResponse
from apps.users.querys import add_user_query, get_user_query, delete_user_query, update_user_query
from apps.users.schemas import UserSchema, UserUpdateSchema
from database.async_connect_postgres import Session, get_session

router = APIRouter(prefix='/users')


@router.post('/add')
async def add_user(user: UserSchema, db: Session = Depends(get_session)):
    query = text(get_user_query).bindparams(user_id=user.user_id)
    cursor = db.execute(query)
    user = cursor.fetchone()
    if user:
        raise HTTPException(status_code=404, detail=f"User with id = {user.user_id} already exists")
    query = text(add_user_query).bindparams(**user.dict())
    await db.execute(query)
    await db.commit()
    return JSONResponse(status_code=201, content={'msg': 'user created'})


@router.get('/{user_id}', response_model=UserSchema)
async def get_user(user_id: int, db: Session = Depends(get_session)):
    query = text(get_user_query).bindparams(user_id=user_id)
    cursor = await db.execute(query)
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.delete('/{user_id}', response_model=UserSchema)
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    query = text(get_user_query).bindparams(user_id=user_id)
    cursor = await db.execute(query)
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id = {user_id} not found")
    query = text(delete_user_query).bindparams(user_id=user_id)
    await db.execute(query)
    await db.commit()
    return JSONResponse(status_code=200, content={'msg': 'user was deleted'})


@router.put('/{user_id}', response_model=UserUpdateSchema)
async def update_user(user: UserUpdateSchema, user_id: int, db: Session = Depends(get_session)):
    query = text(get_user_query).bindparams(user_id=user_id)
    cursor = await db.execute(query)
    check_user = cursor.fetchone()
    if not check_user:
        raise HTTPException(status_code=404, detail=f"User with id = {user_id} not found")
    query = text(update_user_query).bindparams(**user.dict(), user_id=user_id)
    await db.execute(query)
    await db.commit()
    return JSONResponse(status_code=200, content={'msg': 'user was updated'})
