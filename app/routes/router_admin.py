from fastapi import APIRouter,HTTPException
from app.auth.validate import validate_session
from app.auth.createSession import create_temp_session
from app.auth.ManageUser import createUser,deleteUser
from app.schemas.schema import Group
from fastapi import Query
from typing import Optional
router_admin = APIRouter()

@router_admin.post("/{username}/create-user")
async def create_user(username:str,token:str,name:str,selected_group: Optional[Group]=Query()):
    # new_user={
    #    'user':name,
    #    'device_name':device_name,
    #    'user_policy':user_policy
    #}
    temp_session=create_temp_session(validate_session(username,token))
    #print(temp_session)
    await createUser(name,selected_group,temp_session)

@router_admin.delete("/{username}/delete-user")
async def delete_user(username:str,token:str,name:str):
        temp_session=create_temp_session(validate_session(username,token))
        await deleteUser(name,temp_session)
        return {"message": "User deleted successfully"}

    