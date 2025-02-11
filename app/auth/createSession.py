import boto3
from fastapi import HTTPException

def create_temp_session(session):
        temp_session = boto3.session.Session(
            aws_access_key_id=session['access_key_id'],
            aws_secret_access_key=session['secret_access_key'],
            aws_session_token=session['session_token']
        )
        return temp_session

