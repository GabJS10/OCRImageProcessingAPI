from fastapi import APIRouter, HTTPException
from schemas.client import Client
from config.supabase import supabase

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_client(body: Client):
  print(body)
  try:
    res = (supabase
      .table("clients").insert(body.model_dump())
      .execute())

    return res
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

