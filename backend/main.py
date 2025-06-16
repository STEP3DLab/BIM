from __future__ import annotations

import os
import uuid
from pathlib import Path

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, Session

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

DATA_DIR = Path("/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/bim")
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class ScanJob(Base):
    __tablename__ = "scan_jobs"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    status = Column(String, default="uploaded")


Base.metadata.create_all(engine)

app = FastAPI(title="PointCloud API", version="1.0")


@app.post("/v1/scan/job")
async def create_scan_job(file: UploadFile = File(...)) -> JSONResponse:
    job_id = str(uuid.uuid4())
    file_path = DATA_DIR / f"{job_id}_{file.filename}"
    with file_path.open("wb") as buffer:
        content = await file.read()
        buffer.write(content)

    with Session(engine) as session:
        job = ScanJob(id=job_id, filename=file.filename)
        session.add(job)
        session.commit()

    # Placeholder for queueing background job
    return JSONResponse({"job_id": job_id})


@app.get("/v1/scan/job/{job_id}")
def get_scan_job(job_id: str) -> JSONResponse:
    with Session(engine) as session:
        job = session.get(ScanJob, job_id)
        if not job:
            return JSONResponse({"detail": "Job not found"}, status_code=404)
        return JSONResponse({"job_id": job.id, "filename": job.filename, "status": job.status})
