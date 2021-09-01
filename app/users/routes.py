import regex as re
from typing import Optional
from fastapi import APIRouter
from fastapi import responses
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from mongoengine.errors import DoesNotExist, NotUniqueError

from utils.logger import console_logger
from .models import Users
from . import serializers

module_name = "users"
router = APIRouter(
    prefix="/{}".format(module_name.lower()),
    tags=[module_name.lower()]
)

@router.get("")
async def get_users(
        name: Optional[str] = None,
        sort: Optional[str] = "id",
        page: int = 1,
        limit: int = 10,    
    ):
    try:
        if sort == "id":
            sort = "user_id"
        
        if sort == "-id":
            sort = "-user_id"

        users = Users.objects.limit(limit).skip((page-1)*limit).order_by(sort)
        if name is not None:
            users = users(
                __raw__ = {
                    "$or": [
                        {"first_name": {"$regex": ".*{}.*".format(name), "$options": "i"}},
                        {"last_name": {"$regex": ".*{}.*".format(name), "$options": "i"}},
                    ]
                }
            )
        response = [ user.payload() for user in users]
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        console_logger.debug(e)
        raise HTTPException(status_code=500)

@router.get("/{id}")
async def get_user(id: str):
    try:
        user = Users.objects.get(user_id = id)
        return JSONResponse(content=user.payload(), status_code=200)
    except DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        console_logger.debug(e)
        raise HTTPException(status_code=500)

@router.post("")
async def create_user(payload: serializers.create_user):
    try:
        payload = payload.dict(exclude_none=True)
        user_id = payload['id']
        del payload['id']
        user = Users(user_id = user_id, **payload)
        user.save()
        return JSONResponse(content={}, status_code=201)
    except NotUniqueError:
        raise HTTPException(status_code=400)
    except Exception as e:
        console_logger.debug(e)
        raise HTTPException(status_code=500)

@router.put("/{id}")
async def update_user(id: str, payload: serializers.update_user):
    try:
        user = Users.objects.get(user_id = id)
        user.update(**payload.dict(exclude_none=True))
        return JSONResponse(content={}, status_code=200)
    except DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        console_logger.debug(e)
        raise HTTPException(status_code=500)

@router.delete("/{id}")
async def delete_user(id: str):
    try: 
        user = Users.objects.get(user_id = id)
        user.delete()
        return JSONResponse(content={}, status_code=200)
    except DoesNotExist:
        raise HTTPException(status_code=404)
    except Exception as e:
        console_logger.debug(e)
        raise HTTPException(status_code=500)
