from app.config.aws import dynamodb_client,iam_client
from fastapi import HTTPException
import asyncio
async def authenticate_user(username):
    try:       
        table = dynamodb_client.Table('users')
        response = table.get_item(Key={'username': username})
        if not response.get('Item'):
            create_key_response =await asyncio.to_thread(iam_client.create_access_key,UserName=username)
            print(f"Access Key ID: {create_key_response['AccessKey']['AccessKeyId']}")
            print(f"Secret Access Key: {create_key_response['AccessKey']['SecretAccessKey']}")
            try:
                user_data={
                    'username':username,
                    'access_key_id':create_key_response['AccessKey']['AccessKeyId'],
                    'secret_access_key':create_key_response['AccessKey']['SecretAccessKey']
                }
                table.put_item(Item=user_data)
                return user_data
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e)) 
        else:
            print(f"Access Key ID: {response['Item']['access_key_id']}")
            print(f"Secret Access Key: {response['Item']['secret_access_key']}")
            return response['Item']
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    