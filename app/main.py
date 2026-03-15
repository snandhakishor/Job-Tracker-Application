from fastapi import FastAPI
from .database import engine
from . import model
from .routers import jobs

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.include_router(jobs.router)


# @app.get('/jobs')
# def read_jobs(db: Session = Depends(get_db)):
#     jobs = db.execute(text("SELECT company_name, job_title, salary, job_added_at, job_board, job_location, status FROM jobs"))
#     return jobs.mappings().all()


