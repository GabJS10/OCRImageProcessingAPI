from fastapi import APIRouter,UploadFile, File, HTTPException
import cv2
import numpy as np
from config.paddleocr import ocr 
from config.openai import openai
from utils.parse_text import parse_text
import json as JSON

router = APIRouter(
    prefix="/processing",
    tags=["processing"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        results = ocr.predict(input=img)


        for res in results:
          json = res.json


        text = " ".join(json["res"]["rec_texts"])

        prompt = f"""
            context: {text}

            El context es un texto con ruido extraido de una imagen, que contiene informacion personal de una persona.

            Extrae y estructura la informacion personal del context en un texto simple por ejemplo:
            {{
                "nombre": "Juan Perez",
                "cedula": "123456789",
                "lugar_cedula": "Bogota",
                "direccion": "Calle 123",
                "telefono": "3001234567",
                "correo": " H9T9K@example.com",
                "estado_civil": "soltero",
                "tipo_poblacion": "urbana",  
                "nivel_escolaridad": "primaria"
            }}

            Si alguna clave no se encuentra en el texto o es interpretada como ruido, asignale el valor null.

            Ya que el texto es muy ruidoso, intenta extraer la mayor cantidad de informacion posible, corrigiendo errores pero sin inventar datos.

        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                    {"role": "system", "content": "Eres un asistente que extrae informacion personal de textos ruidosos."},
                {"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.2,
        )
        text = response.choices[0].message.content
        
        return {"data":JSON.loads(text)} 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {e}")
    

