# app/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"

@app.get("/")
def root():
    return {"Hello" : "World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return JSONResponse(content={"message": "File uploaded successfully", "filename": file.filename})
