from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from app.database import init_db
import os
import shutil
from app.fileparser import parse_file
from icalendar import Calendar, Event
from fastapi.responses import FileResponse


app = FastAPI()

knownAssignments = []
unknownAssignments = []

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

@app.get("/calendar")
def generate_calendar():
    times = []
    cal = Calendar()
    for i in range(len(knownAssignments)):
        event = Event()
        event.add('summary', knownAssignments[i].get("course_name") + " " + knownAssignments[i].get("assignment_title"))
        date_str = knownAssignments[i].get("due_date")
        index = -1
        for j, char in enumerate(date_str):
            if char.isdigit():
                index = j
                break
        if(index != -1):
            date_str = date_str[index:]
        eventtime = datetime.strptime(date_str, "%Y-%m-%d")
        times.append(eventtime.strftime("%d/%m/%Y"))
        event.add('dtstart', eventtime)
        duration = timedelta(days=1)
        event.add('dtend', eventtime+duration)
        cal.add_component(event)
    file_location = os.path.join(UPLOAD_DIR, "assignmentcalender.ics")
    with open(file_location, "wb") as f:
            f.write(cal.to_ical())
    return FileResponse(file_location, media_type='text/calendar', filename="assignmentcalendar.ics")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        assignments = parse_file(file_location)
        os.remove(file_location)

        for i in range(len(assignments)):
            if not isinstance(assignments[i], dict):
                unknownAssignments.append({"error": "Malformed entry", "raw": assignments[i]})
                continue

            date_str = assignments[i].get("due_date")
            index = -1
            for j, char in enumerate(date_str):
                if char.isdigit():
                    index = j
                    break
            if(index != -1):
                date_str = date_str[index:]
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                knownAssignments.append(assignments[i])
            except ValueError:
                unknownAssignments.append(assignments[i])
        return {"message": "File uploaded and parsed successfully",
                "total assignemnts": assignments,
                "dated assignments": knownAssignments,
                "undated assignments": unknownAssignments,
                "number of known assignments": len(knownAssignments)}
    except Exception as e:
        return {"error": str(e)}
