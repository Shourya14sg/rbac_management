import boto3
from fastapi import HTTPException

def create_temp_session(session):
    try:
        temp_session = boto3.session.Session(
            aws_access_key_id=session['access_key_id'],
            aws_secret_access_key=session['secret_access_key'],
            aws_session_token=session['session_token']
        )
        return temp_session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating temporary session: {str(e)}")

