import boto3
from botocore.config import Config

# AWS S3 配置
S3_CONF = {
    'aws_access_key_id': '******',
    'aws_secret_access_key': '******',
    'region_name': '******',
    'bucket_name': '******',
}


def _get_s3_client():
    my_config = Config(region_name=S3_CONF['region_name'])

    endpoint_url = 'https://s3.{}.amazonaws.com'.format(S3_CONF['region_name'])
    return boto3.client('s3', config=my_config, endpoint_url=endpoint_url,
                        aws_access_key_id=S3_CONF['aws_access_key_id'],
                        aws_secret_access_key=S3_CONF['aws_secret_access_key'])


def _gen_pre_url(client_method, object_name, expires_in=60):
    params = {
        'Bucket': S3_CONF['bucket_name'],
        'Key': object_name
    }

    return _get_s3_client().generate_presigned_url(
        ClientMethod=client_method, Params=params, ExpiresIn=expires_in)


def gen_upload_url(object_name, expires_in=60):
    # 生成文件上传地址
    return _gen_pre_url('put_object', object_name, expires_in)


def gen_download_url(object_name, expires_in=60):
    # 生成文件下载地址
    return _gen_pre_url('get_object', object_name, expires_in)


def upload_file(f, object_name: str):
    # 文件上传
    return _get_s3_client().upload_fileobj(f, S3_CONF['bucket_name'], object_name)
