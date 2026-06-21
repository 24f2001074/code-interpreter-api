from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import traceback
from io import StringIO
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/code-interpreter")
def code_interpreter(req: CodeRequest):
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(req.code)
        output = sys.stdout.getvalue()

        return {
            "error": [],
            "result": output
        }

    except Exception:
        tb = traceback.format_exc()

        matches = re.findall(r'File "<string>", line (\d+)', tb)

        error_line = []
        if matches:
            error_line = [int(matches[-1])]

        return {
            "error": error_line,
            "result": tb
        }
