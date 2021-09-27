from snakecraft import TerraformBlock

# Configure the state backend
TerraformBlock(
    backend=dict(
        s3=dict(
            bucket="mybucket",
            key="path/to/statefile",
            region="us-east-1",
        )
    )
)
