from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
import os
import shutil
from app.fileparser import parse_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"

@app.on_event("startup")
async def startup_event():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    init_db()


@app.get("/")
def root():
    return {"Hello" : "World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        assignments = parse_file(file_location)

        return {"message": "File uploaded and parsed successfully",
                "filename": file.filename,
                "assignments": assignments}
    except Exception as e:
        return {"error": str(e)}
