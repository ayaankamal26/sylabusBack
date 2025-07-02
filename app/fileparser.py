import ollama
import os
import json
from typing import List, Dict
import pdfplumber
import docx



def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def parse_file(file_path: str) -> List[dict]:
    ext = os.path.splitext(file_path.lower())
    if ext[1] == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext[1] == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"File must be in .pdf or .docx form: {ext}")
    assignments = run_local_llm_parser(text)

    return assignments


def run_local_llm_parser(text: str) -> list[dict]:
    prompt = f"""
Read the following syllabus and extract all assignments and exams. If the date given in the sylabus does not contain a year. Assume the year is the next time
that date will occur. Today is July 2, 2025.

Return a JSON array with each entry having:
- title
- due_date (YYYY-MM-DD format)

Syllabus:
\"\"\"
{text}
\"\"\"
"""

    response = ollama.chat(
        model='mistral',
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response['message']['content'])
    except json.JSONDecodeError:
        print("Could not parse JSON output")
        return []
