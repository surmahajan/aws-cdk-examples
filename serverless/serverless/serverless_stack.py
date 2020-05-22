from aws_cdk import (
    aws_s3 as s3,
    core
)


class ServerlessStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        publicAccess = s3.BlockPublicAccess(block_public_acls=True, block_public_policy=True, ignore_public_acls=True,
                                            restrict_public_buckets=True)
        bucket = s3.Bucket(self,
                           "cdk-bucket",
                           versioned=True, block_public_access=publicAccess)
