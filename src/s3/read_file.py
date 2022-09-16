import boto3
from awscli.customizations.s3.utils import split_s3_bucket_key
import streamlit as st 

s3 = boto3.client('s3', aws_access_key_id=st.secrets['aws_public_key'],
                  aws_secret_access_key=st.secrets['aws_secret_key'])


def download_s3_file(url, local_file, s3=s3):
    bucket_name, prefix = split_s3_bucket_key(url)
    try:
        s3.download_file(bucket_name, prefix, local_file)
        return 200
    except Exception as e:
        return e
        