import boto3
from awscli.customizations.s3.utils import split_s3_bucket_key
import streamlit as st 


s3 = boto3.client('s3', aws_access_key_id=st.secrets['aws_public_key'],
                  aws_secret_access_key=st.secrets['aws_secret_key'])


def upload_s3_file(local_file, url, s3=s3, make_public=False):
    bucket_name, prefix = split_s3_bucket_key(url)
    if make_public:
        s3.upload_file(local_file, bucket_name, prefix,
                       ExtraArgs={'ACL': 'public-read'})
    else:
        s3.upload_file(local_file, bucket_name, prefix)