from fastapi import APIRouter,HTTPException
import boto3
from app.config.aws import session 
from app.auth.validate import validate_session
from app.auth.createSession import create_temp_session

router_viewer = APIRouter()
@router_viewer.get('/')
async def index():
    return {"message": "Welcome to the viewer page."}

@router_viewer.get("/{username}/log-viewer")
async def get_logs(username:str,token:str):
    temp_session=create_temp_session(validate_session(username,token))
    print(temp_session)
    try:
        cloudtrail_client = temp_session.client('cloudtrail',region_name='ap-south-1')
        # Logic to fetch logs from CloudTrail (specific configuration required)
        
        events = cloudtrail_client.lookup_events()#log_group_name='CloudTrail',log_stream_name='CloudTrail/DefaultLogGroup')
        print(events)
        raise HTTPException(status_code=200, detail="Logs retrieved.")
        #return {"message": "Logs retrieved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Logs retrieved."}


