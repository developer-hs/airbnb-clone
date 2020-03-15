from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "static/"
    file_overwrite = False  # 같은파일 존재 할 경우 덮어쓰기 안함(건너뛰기)


class UploadStorage(S3Boto3Storage):
    location = "uploads/"
