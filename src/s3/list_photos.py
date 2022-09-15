import boto3
from awscli.customizations.s3.utils import split_s3_bucket_key
import streamlit as st 


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


def list_bucket(dir_s3_path, s3=s3):
    """
    Returns all the files stored in s3 bucket in a list type.
    :param dir_s3_path: the s3 path of the bucket.
    """
    bucket_name, prefix = split_s3_bucket_key(dir_s3_path)
    box = []
    for file in get_all_s3_objects(s3, Bucket=bucket_name, Prefix=prefix):
        box.append(file)
    return(box)
