from fastapi import APIRouter,Form,HTTPException
from app.auth.auth_user import authenticate_user
#from app.config.aws import iam_client#,sts_client
from app.config.aws import session as aws_session, iam_client,dynamodb_client

router_auth = APIRouter()
#get user from aws iam it will take mfa code and user name for password validation we have to check if the user is in the database so need to create db user table

@router_auth.post("/login")
async def login(username:str=Form(...),mfa_code:str=Form(...)):
     #get user from aws iam
    try:
       #user exists?
        user = iam_client.get_user(UserName=username)
        res=await authenticate_user(username)
        mfa_device = iam_client.list_mfa_devices(UserName=username)
        if not mfa_device['MFADevices']:
            raise HTTPException(status_code=403, detail="Forbidden: MFA not enabled for this user")
        
        mfa_serial=mfa_device['MFADevices'][0]['SerialNumber']

        sts_client = aws_session.client('sts',
                                        aws_access_key_id=res['access_key_id'],
                                        aws_secret_access_key=res['secret_access_key'],
                                        region_name='ap-south-1')
        #response = sts_client.get_caller_identity()  
        try:
            session = sts_client.get_session_token(
                SerialNumber=mfa_serial,
                TokenCode=mfa_code
            #    ,DurationSeconds=123 # 15 minutes session
            )
            try:
                table=dynamodb_client.Table('user_session')
                result = {
                    'username': username,
                    'expiry_time': session['Credentials']['Expiration'].isoformat(),  # Convert datetime to ISO 8601 string
                    'access_key_id':session['Credentials']['AccessKeyId'],
                    'secret_access_key':session['Credentials']['SecretAccessKey'],
                    'session_token':session['Credentials']['SessionToken']
                }
                table.put_item(Item=result)
            except Exception as e:
                print(e)
                raise HTTPException(status_code=500, detail="dynamodb error in creating session")
            return result #session['Credentials']   #main thing for session manangement
        
        except iam_client.exceptions.ClientError as e:
           raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router_auth.get("/logout")
async def logout(username:str):
    try:
        table=dynamodb_client.Table('user_session')
        table.delete_item(Key={'username': username})
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

