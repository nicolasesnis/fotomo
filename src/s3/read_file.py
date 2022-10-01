import boto3
from awscli.customizations.s3.utils import split_s3_bucket_key
import streamlit as st 
import pandas as pd
from io import StringIO


s3 = boto3.client('s3', aws_access_key_id=st.secrets['aws_public_key'],
                  aws_secret_access_key=st.secrets['aws_secret_key'])

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
        