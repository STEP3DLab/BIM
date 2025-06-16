from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

DATA_DIR = Path("/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="PointCloud API", version="1.0")


@app.post("/v1/scan/job")
async def create_scan_job(file: UploadFile = File(...)) -> JSONResponse:
    job_id = str(uuid.uuid4())
    file_path = DATA_DIR / f"{job_id}_{file.filename}"
    with file_path.open("wb") as buffer:
        content = await file.read()
        buffer.write(content)
    # Placeholder for queueing background job
    return JSONResponse({"job_id": job_id})
