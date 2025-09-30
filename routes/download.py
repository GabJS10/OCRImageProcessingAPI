from fastapi import APIRouter, HTTPException
from schemas.client import Client
from config.supabase import supabase
from io import BytesIO
from openpyxl import Workbook
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/download",
    tags=["download"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def download_data_in_excel():
  try:
    res = (supabase
      .table("clients").select("nombre,cedula,lugar_cedula,direccion,telefono,correo,estado_civil,tipo_poblacion,nivel_escolaridad")
      .execute())
    
    data = res.data

    if not data:
      raise HTTPException(status_code=404, detail="No data found")

    wb = Workbook()
    ws = wb.active
    ws.title = "Clients"

    headers = data[0].keys()  
    ws.append(list(headers))

    for item in data:
        ws.append(list(item.values()))

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)

    return StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=clients.xlsx"})
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))