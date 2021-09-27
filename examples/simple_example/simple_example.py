from snakecraft import Output, Parameter, Provider, ResourceName, TerraformBlock

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


AWS = Provider("aws", region="us-east-1")


class DebianAMI(AWS.Data.ami):
    most_recent = True
    owners = ["136693071363"]
    name_regex = r"^debian-10-amd64-\d{8}-\d{3}$"


def make_cluster():
    debian_ami = DebianAMI()

    class DebianMachine(AWS.Resource.instance):
        ami = debian_ami
        instance_type = "t3.micro"
        key_name = Parameter("key_name", None)
        tags = dict(Name=ResourceName)  # Will tag the AWS resource with it's internal name

    class BigDebianMachine(DebianMachine):
        instance_type = "t3.xlarge"

    small_machines = [DebianMachine(i) for i in range(5)]
    big_machines = [BigDebianMachine(i, key_name="johndoe") for i in range(2)]

    Output("small_machine_arns", value=[server.arn for server in small_machines])
    Output("big_machine_arns", value=[server.arn for server in big_machines])
