from snakecraft import Provider

# Including support multiple aliased instances of the same provider
AWS = Provider("aws", region="us-east-1")
AWS_West = Provider("aws", region="us-west-1", alias="west")
