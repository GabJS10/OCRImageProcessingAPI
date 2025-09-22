from pydantic import BaseModel, Field, EmailStr, field_validator 
from typing import Optional

class Client(BaseModel):
    nombre: str
    #cedula max 10 caracteres
    cedula: str = Field(..., max_length=10, min_length=8,description="Cedula de 10 digitos")
    lugar_cedula: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado_civil: Optional[str] = None
    tipo_poblacion: Optional[str] = None
    nivel_escolaridad: Optional[str] = None

    @field_validator('telefono')
    def validate_telefono(cls, v):
        if v is None:
            return v
        if not v.isdigit() or len(v) < 10 or len(v) > 10:
            raise ValueError('Telefono debe contener solo digitos y 10 caracteres')
        return v