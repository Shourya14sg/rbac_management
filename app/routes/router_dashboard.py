from fastapi import APIRouter,HTTPException
from app.auth.validate import validate_session
from app.auth.createSession import create_temp_session

router_dashboard = APIRouter()

@router_dashboard.get("/{username}")
async def get_dashboard(username:str,token:str):
    try:
        session=validate_session(username,token)
    except Exception as e:
        raise HTTPException(status_code=402, detail="invalid credentials")
    
    try:
        temp_session = create_temp_session(session)

        iam_client = temp_session.client('iam')
        # Get IAM user details
        user = iam_client.get_user()
        # Get IAM groups for the user
        groups = iam_client.list_groups_for_user(UserName=username)

        # Get attached policies for the user
        attached_policies = iam_client.list_attached_user_policies(UserName=username)

        # Get inline policies for the user
        inline_policies = iam_client.list_user_policies(UserName=username)

        # Gather permissions granted via groups
        group_permissions = []
        curr_group=[]
        for group in groups['Groups']:
            group_name = group['GroupName']
            curr_group.append(group_name)
            group_policies = iam_client.list_attached_group_policies(GroupName=group_name)
            group_permissions.append({
                "group_name": group_name,
                "permissions": [policy['PolicyName'] 
                                      for policy in group_policies['AttachedPolicies'] 
                                      if policy['PolicyName'] !='BackendAccess'
                                      ]
            })

        return {
            "username": username,
            "Assigned_group":curr_group,
            "attached_policies": attached_policies['AttachedPolicies'],
            "inline_policies": inline_policies['PolicyNames'],
            "permissions": group_permissions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching IAM details: {str(e)}")