import boto3
import streamlit as st 

s3 = boto3.resource('s3', aws_access_key_id=st.secrets['aws_public_key'],
                  aws_secret_access_key=st.secrets['aws_secret_key'])
def copy_s3_object(source_bucket, source_key, dest_bucket, dest_key):
    copy_source = {
        'Bucket': source_bucket,
        'Key': source_key
        }
    bucket = s3.Bucket(dest_bucket)
    return bucket.copy(copy_source, dest_key)