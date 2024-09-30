from storages.backends.s3boto3 import S3Boto3Storage


class PrivateUploadStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = True
    auto_create_bucket = True


class PublicUploadStorage(S3Boto3Storage):
    location = 'public'
    # default_acl = 'public-read'
    file_overwrite = True
    auto_create_bucket = True
