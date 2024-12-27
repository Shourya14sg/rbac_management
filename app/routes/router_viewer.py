from fastapi import APIRouter,HTTPException
import boto3
from app.config.aws import session 
from app.auth.validate import validate_session

router_view = APIRouter()


@router_view.get("/{username}/get-logs")
async def get_logs(username:str,token:str):
    credentials = validate_session(username,token)
    try:
        logs_client = boto3.client('logs',
                                   aws_access_key_id=credentials['access_key_id'],
                                   aws_secret_access_key=credentials['secret_access_key'],
                                   region_name='ap-south-1')#, region_name='YOUR_REGION')
        # Logic to fetch logs from CloudTrail (specific configuration required)
        events = logs_client.get_log_events(log_group_name='CloudTrail',log_stream_name='CloudTrail/DefaultLogGroup')
        print(events)
        return {"message": "Logs retrieved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



