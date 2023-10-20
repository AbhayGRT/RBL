import boto3
import os
import datetime

def upload_image_to_s3_with_date_structure(image_path, s3_bucket, aws_access_key_id, aws_secret_access_key):
    try:
        # Initialize the S3 client
        s3 = boto3.client('s3', 
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        
        today = datetime.date.today()
        date_folder = today.strftime('%Y-%m-%d')
        
        # Create the folder structure if it doesn't exist
        s3_folder = f'{date_folder}/'
        s3_key = f'{s3_folder}{os.path.basename(image_path)}'
        
        s3.upload_file(image_path, s3_bucket, s3_key)
        s3_url = f'https://{s3_bucket}.s3.amazonaws.com/{s3_key}'  # Construct the S3 URL
        return s3_url
    except Exception as e:
        return f'Error: {str(e)}'

# Specify the local image file to upload
local_image_path = '/home/abhay/Documents/cheque.png'
aws_access_key_id = 'AKIAQPMTCHZSYHM7KUON'
aws_secret_access_key = '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'
bucket_name = 'chequeimages'

# Upload the image to S3 with a date-based folder structure and get the S3 link
s3_link = upload_image_to_s3_with_date_structure(local_image_path, bucket_name, aws_access_key_id, aws_secret_access_key)
print(s3_link)
