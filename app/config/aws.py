import os
from  dotenv import load_dotenv
import boto3

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
# Load the .env file
load_dotenv(dotenv_path)


session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
iam_client = session.client('iam')
dynamodb_client = session.resource('dynamodb',region_name='ap-south-1')
#dynamodb_client = session.client('dynamodb')
#sts_client = boto3.client('sts')


#aws_access_key_id='AKIA44Y6CC26RT3TM6RD',
#  aws_secret_access_key='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')
  