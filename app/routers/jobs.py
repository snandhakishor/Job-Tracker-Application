from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends
from typing import List, Optional
from .. import model
from ..schemas import JobsOut, Jobs, CreateJobs
from ..database import get_db

router = APIRouter(
    prefix='/jobs',
    tags=['Jobs']
)

@router.get('/jobs/inactive-jobs')
def read_root(db: Session = Depends(get_db)):
    no_response_job = db.execute(text(
        "SELECT id, company_name, job_title, salary, job_added_at, job_board, job_location FROM jobs WHERE datediff(now(), job_added_at) > 14 AND status = 'pending'"
    ))
    jobs = no_response_job.mappings().all()
    if not jobs:
        return "Currently no inactive jobs (applied more than 14 days ago)"
    else:
        return "these could be the jobs you have not heard back from, you can follow up with them or change the status to 'rejected' if you are no longer interested in the job", jobs

@router.get('/jobs/last-applied', response_model=List[JobsOut])
def get_last_ones(db: Session = Depends(get_db), page_num: int = 1):
    last_jobs = db.query(model.Job).order_by(model.Job.job_added_at.desc()).limit(page_num*10).offset((page_num-1)*10).all()
    return last_jobs


@router.post('/jobs')
def create_job(job: Jobs, db: Session = Depends(get_db)):
    new_job = model.Job(**job.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.delete('/jobs/{job_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    delete_job = db.query(model.Job).filter(model.Job.id == job_id).first()
    if delete_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Job not found")
    db.delete(delete_job)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/jobs/search-jobs')
def search_jobs(jobs = Jobs, db: Session = Depends(get_db), company_name: Optional[str] = "", 
                job_title: Optional[str] = ""):
    available_jobs = db.query(model.Job).filter(model.Job.company_name.contains(company_name),
                                                model.Job.job_title.contains(job_title))
    if len(list(available_jobs))==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Job not found")
    return available_jobs.all()

@router.patch('/jobs/{id}', status_code=status.HTTP_201_CREATED)
def update_jobs(id: int, jobs: CreateJobs, db: Session = Depends(get_db)):
    the_job = db.query(model.Job).filter(model.Job.id == id)
    if not the_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Job with id: {id} not found')
    the_job.update(jobs.model_dump(exclude_unset=True))
    db.commit()
    return the_job.first()