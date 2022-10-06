import boto3
from botocore.client import Config
from awscli.customizations.s3.utils import split_s3_bucket_key
import streamlit as st 
import pandas as pd
from io import StringIO


s3 = boto3.client('s3', 
                  aws_access_key_id=st.secrets['aws_public_key'],
                  aws_secret_access_key=st.secrets['aws_secret_key'], 
                  config=Config(signature_version='s3v4'),
                  region_name='eu-west-3')

s3_resource = boto3.resource('s3', aws_access_key_id=st.secrets['aws_public_key'],
                  aws_secret_access_key=st.secrets['aws_secret_key'])


def download_s3_file(url, local_file, s3=s3):
    bucket_name, prefix = split_s3_bucket_key(url)
    try:
        s3.download_file(bucket_name, prefix, local_file)
        return 200
    except Exception as e:
        return e

def read_s3_df_file(url, s3=s3_resource):
    bucket_name, prefix = split_s3_bucket_key(url)
    try:
        l = s3.Object(bucket_name, prefix).get()['Body'].read().decode().split('\n')
        l = [i.split(',') for i in l]
        df = pd.DataFrame(l)
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        return df
    except Exception as e:
        return e



def create_presigned_url(bucket_name, object_name, expiration=3600, s3_client=s3):    
    
    response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)

    # The response contains the presigned URL
    return response
