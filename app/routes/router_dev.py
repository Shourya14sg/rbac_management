from fastapi import APIRouter,HTTPException
from app.utils.createBucket import create_s3_bucket
from app.auth.validate import validate_session
from app.auth.createSession import create_temp_session

router_dev=APIRouter()

@router_dev.get("/{username}/create-bucket")
async def create_bucket(username:str,token:str,bucket_name:str):
    temp_session=create_temp_session(validate_session(username,token))
    create_s3_bucket(bucket_name,temp_session)
    return {"message": "Bucket created successfully"}