import boto3
from flask import current_app

def upload_img(file_name, object_name):

    s3_client = boto3.client( "s3",
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )

    s3_client.put_object(
            Key=file_name,
            Bucket=current_app.config['AWS_BUCKET_NAME'],
            Body=object_name,
            ContentType ='image/jpeg',
            ACL= 'public-read'
            
        )
    #upload_file(file_name, current_app.config['AWS_BUCKET_NAME'], object_name)
    #return response

def show_img():

    s3_client = boto3.client( "s3",
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )
    return current_app.config['AWS_BUCKET_PIC']