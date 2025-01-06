from fastapi import HTTPException
def create_s3_bucket(bucket_name,temp_session):
    try:
        s3_client = temp_session.client('s3',region_name='ap-south-1')
    except Exception as e:
        raise HTTPException(status_code=403, detail="Forbidden: Permission Denied!! ")
    try:
        # Create the S3 bucket
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'  # Choose your region
            }
        )
        #raise HTTPException(status_code=200, detail="Bucket created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Bucket created successfully"}