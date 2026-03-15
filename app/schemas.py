from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class Jobs(BaseModel):
    company_name: str
    job_title: str
    salary: Optional[int] = None
    job_board: Optional[str] = None
    job_location: Optional[str] = None
    applied: Optional[str] = "yes"
    status: Optional[str] = "pending"
    job_added_at: Optional[datetime] = datetime.now()

class JobsOut(Jobs):
    pass
    

class CreateJobs(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    salary: Optional[int] = None
    job_board: Optional[str] = None
    job_location: Optional[str] = None
    applied: Optional[str] = None
    status: Optional[str] = None
    