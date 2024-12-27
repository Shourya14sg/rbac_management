from fastapi import HTTPException
from datetime import datetime
from app.config.aws import dynamodb_client  
def validate_session(username,token):
    try:
        table = dynamodb_client.Table('user_session')
        response = table.get_item(Key={'username': username})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Session not found")
        session = response['Item']
        # Parse expiry_time 
        expiry_time = datetime.isoformat(datetime.fromisoformat(session['expiry_time']))
        
        if expiry_time < datetime.now().isoformat():#datetime.timezone.utc):
            table.delete_item(Key={'username': username})
            raise HTTPException(status_code=403, detail="Session expired")
        
        if token != session['session_token']:
            raise HTTPException(status_code=403, detail="bad request/Token mismatch")
        #print("session",session)
        return session
    except Exception as e:
        print("Error in validate_session:",e)
        raise HTTPException(status_code=403, detail=str(e))
    