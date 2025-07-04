# Syllabus Assignment Calendar Backend

This is the Python/FastAPI backend for the Syllabus Assignment Calendar, a tool that allows students to upload course syllabi (PDF or DOCX), parse out assignments and exams, and generate a downloadable `.ics` calendar file compatible with Google Calendar, Apple Calendar, Outlook, and more.

---

## Features

- Upload syllabi via drag-and-drop or file picker.
- View a list of uploaded syllabus files.
- Generate a downloadable `.ics` calendar file from parsed assignments.
- Integrates seamlessly with a FastAPI backend that uses LLMs to parse syllabus content.

---

## How It Works

1. User uploads a syllabus document (PDF or Word).
2. The file is sent to the FastAPI backend, which uses a local LLM to extract assignment titles and due dates.
3. The backend creates an `.ics` file from the recognized due dates.
4. The frontend allows the user to download the generated calendar.

---

## Tech Stack

- **Frontend (separate repo)**: React (TypeScript)
- **Backend**: FastAPI + Ollama + PDF/DOCX parsing
- **Calendar Format**: iCalendar (`.ics`) standard

---

## To Run

1. Clone repository
2. Set up a virtual environment and download dependencies
3. Run Ollama on local machine
4. Run the server using uvicorn
