from storages.backends.s3boto3 import S3Boto3Storage


class NetCDFMinioStorage(S3Boto3Storage):
    default_acl = "private"
    file_overwrite = True
    custom_domain = False

    def read_netcdf(self, name):
        with self.open(name, mode="rb") as f:
            return f.read()
