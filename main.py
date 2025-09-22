from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.processing import router as processing_router
from routes.clients import router as clients_router
from routes.download import router as download_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
app = FastAPI(
    title="My API",
    description="This is a sample API",
    version="1.0.0",  
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes, ajusta esto según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)   

app.include_router(processing_router)
app.include_router(clients_router)
app.include_router(download_router)


app.mount("/static", StaticFiles(directory="src"), name="static")


@app.get("/")
async def read_root():
    return FileResponse("src/index.html")