import re

def parse_text(text):
    data = {}

    nombre = re.search(r"Nombre\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+)", text)
    if nombre: data["nombre"] = nombre.group(1).strip()

    cedula = re.search(r"C\.?C\.?N0[_\s]*([0-9]+)\s+de\s+([A-Za-z\s]+)", text)
    if cedula:
        data["cedula"] = cedula.group(1).strip()
        data["lugar de cedula"] = cedula.group(2).strip()

    telefono = re.search(r"Tel[eé]fono[_\s]*([0-9]+)", text)
    if telefono: data["telefono"] = telefono.group(1).strip()

    correo = re.search(r"Correo\s+([^\s]+@[^\s]+)", text)
    if correo: data["correo"] = correo.group(1).lower()

    estado = re.search(r"Estado civil\s+([A-Za-z]+)", text)
    if estado: data["estado civil"] = estado.group(1).lower()

    poblacion = re.search(r"poblaci[oó]n\s+([A-Za-z]+)", text)
    if poblacion: data["tipo de poblacion"] = poblacion.group(1).capitalize()

    escolaridad = re.search(r"escolaridad\s+([A-Za-z]+)", text)
    if escolaridad: data["nivel de escolaridad"] = escolaridad.group(1).lower()

    return data
