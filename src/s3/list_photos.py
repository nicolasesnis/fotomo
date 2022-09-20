import boto3
import shutil
from awscli.customizations.s3.utils import split_s3_bucket_key
import streamlit as st 
import pickle
import os
import pandas as pd

s3 = boto3.client('s3', aws_access_key_id=st.secrets['aws_public_key'],
                  aws_secret_access_key=st.secrets['aws_secret_key'])


def get_all_s3_objects(s3, **base_kwargs):
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield from response.get('Contents', [])
        if not response.get('IsTruncated'):  # At the end of the list?
            break
        continuation_token = response.get('NextContinuationToken')


def list_bucket(dir_s3_path, s3=s3, reduce_aws_usage=True):
    """
    Returns all the files stored in s3 bucket in a list type.
    :param dir_s3_path: the s3 path of the bucket.
    """
    today = str(pd.to_datetime('today').date())
    key = dir_s3_path.replace('s3://', '').replace('/', '_') # s3 directory being listed
    dir = 'src/s3/data/list_photos/' + key + '/'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    if today not in os.listdir(dir) or not reduce_aws_usage:
        shutil.rmtree(dir) # remove past files
        os.mkdir(dir)
        bucket_name, prefix = split_s3_bucket_key(dir_s3_path)
        box = []
        for file in get_all_s3_objects(s3, Bucket=bucket_name, Prefix=prefix):
            box.append(file)
        with open(dir + today, 'wb') as fp:
            pickle.dump(box, fp)
    else:
        with open(dir + today, 'rb') as fp:
            box = pickle.load(fp)
    return(box)
