import os
import json
import webbrowser
from fastapi import HTTPException
from app.auth.auth_user import authenticate_user

async def createUser(unique_name,group_name,temp_session):
    #print(unique_name["user"])
    try:
        dynamodb_client = temp_session.resource('dynamodb',region_name='ap-south-1')
        table = dynamodb_client.Table('users')
        res= table.get_item(Key={'username': unique_name})
        if res.get('Item'):                    
            raise HTTPException(status_code=403, detail="Forbidden: User already exists")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized: "+str(e))
        
    try:
        iam_client = temp_session.client('iam')
        iam_resource = temp_session.resource('iam')
        user = iam_resource.create_user(UserName=unique_name)
        print(f"Created user :{user.name}.")
    except iam_client.exceptions.EntityAlreadyExistsException as e:
        #iam_resource.delete_user(UserName=unique_name["user"])
        raise HTTPException(status_code=403, detail="Forbidden: User already exists")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized access"+str(e))
    try:
        device_name=input("Enter the device name: ")
        virtual_mfa_device = iam_resource.create_virtual_mfa_device(
            VirtualMFADeviceName=device_name
        )
        print(f"Created virtual MFA device {virtual_mfa_device.serial_number}")
    
        print(f"Showing the QR code for the device. Scan this in the MFA app of your choice.")
        with open("qr.png", "wb") as qr_file:
            qr_file.write(virtual_mfa_device.qr_code_png)
        webbrowser.open(qr_file.name)

        print(f"Enter two consecutive code from your MFA device.")
        mfa_code_1 = input("Enter the first code: ")
        mfa_code_2 = input("Enter the second code: ")
        user.enable_mfa(
            SerialNumber=virtual_mfa_device.serial_number,
            AuthenticationCode1=mfa_code_1,
            AuthenticationCode2=mfa_code_2,
        )
        os.remove(qr_file.name)
        print(f"MFA device is registered with the user.")
    except Exception as e:
        raise HTTPException(status_code=403, detail="Failed to register MFA device"+str(e))
    try:
        iam_client.attach_user_policy(
            PolicyArn="arn:aws:iam::886436927165:policy/MFARequiredPolicy",
            UserName=unique_name
        )
        iam_client.add_user_to_group(
            GroupName=group_name,
            UserName=unique_name
        )
        res=await authenticate_user(unique_name)
    except Exception as e:
        raise HTTPException(status_code=403, detail="Failed to attach policy"+str(e))
    raise HTTPException(status_code=200, detail="User created successfully")

async def deleteUser(unique_name,temp_session):
    try:
        dynamodb_client = temp_session.resource('dynamodb',region_name='ap-south-1')
        table = dynamodb_client.Table('users')
        res= table.get_item(Key={'username': unique_name})
        if not res.get('Item'):
            raise HTTPException(status_code=403, detail="Forbidden: User does not exist")
        iam_client = temp_session.client('iam')
        iam_resource = temp_session.resource('iam')
        try:
            # Detach all managed policies
            for policy in iam_client.list_attached_user_policies(UserName=unique_name)['AttachedPolicies']:
                iam_client.detach_user_policy(UserName=unique_name, PolicyArn=policy['PolicyArn'])
                print(policy)
        except Exception as e:
            raise HTTPException(status_code=403, detail="Failed to detach policy"+str(e))

        # Remove all inline policies
        try:
            for policy_name in iam_client.list_user_policies(UserName=unique_name)['PolicyNames']:
                iam_client.delete_user_policy(UserName=unique_name, PolicyName=policy_name)
        except Exception as e:
            raise HTTPException(status_code=403, detail="Failed to delete inline policy"+str(e))

        # Delete access keys
        try:
            for key in iam_client.list_access_keys(UserName=unique_name)['AccessKeyMetadata']:
                iam_client.delete_access_key(UserName=unique_name, AccessKeyId=key['AccessKeyId'])
        except Exception as e:
            raise HTTPException(status_code=403, detail="Failed to delete access key"+str(e))
        
        try:
            for group in iam_client.list_groups_for_user(UserName=unique_name)['Groups']:
                iam_client.remove_user_from_group(UserName=unique_name, GroupName=group['GroupName'])
        except Exception as e:
            raise HTTPException(status_code=403, detail="Failed to remove user from group"+str(e))

        try:
            for mfa_device in iam_client.list_mfa_devices(UserName=unique_name)['MFADevices']:
                iam_client.deactivate_mfa_device(UserName=unique_name, SerialNumber=mfa_device['SerialNumber'])
                iam_resource.delete_mfa_device(UserName=unique_name, SerialNumber=mfa_device['SerialNumber'])
        except Exception as e:
            raise HTTPException(status_code=403, detail=f"Failed to remove MFA device: {e}")

        # Delete the login profile (if exists)
        try:
            iam_client.delete_login_profile(UserName=unique_name)
        except Exception as e:
            raise HTTPException(status_code=403, detail="Failed to delete login profile"+str(e))

        # Finally, delete the user
        try:
            iam_client.delete_user(UserName=unique_name)
        except Exception as e:
            raise HTTPException(status_code=403, detail="Failed to delete user"+str(e))
        table.delete_item(Key={'username': unique_name})
    
    except Exception as e:
        print(f"Error deleting user '{unique_name}': {e}")
        raise HTTPException(status_code=403, detail=str(e))

    print(f"User '{unique_name}' deleted successfully.")
    raise HTTPException(status_code=200, detail="User deleted successfully")