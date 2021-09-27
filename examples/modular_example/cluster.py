from snakecraft import Deferred, Module, Output, Parameter, ResourceName, TFModule

from .db import make_db_module
from .providers import AWS, AWS_West
from .util import hvm_filter


class UbuntuAMI(AWS.Data.ami):
    most_recent = True
    owners = ["099720109477"]  # Canonical

    class filter:
        name = "name"
        values = [Parameter("ubuntu_image_name")]

    # Repeating a definition works totally fine.
    # This adds a second filter section to the AMI:
    filter = hvm_filter


class UbuntuMachineUsingDeferred(AWS.Resource.instance):
    """Similar to UbuntuMachine below, just in module context with a Parameter."""

    ami = UbuntuAMI("example_ami", ubuntu_image_name="foo")

    class provisioner:
        "local-exec"
        command = Deferred(
            lambda r: f"echo Connecting to the DB ({Parameter('db_module').db.public_ip(r)})"
        )


def make_cluster(config):
    ubuntu_ami = UbuntuAMI(ubuntu_image_name=config.ubuntu_image_name)
    db_module = make_db_module(config, ubuntu_ami)

    class UbuntuMachine(AWS.Resource.instance):
        ami = ubuntu_ami
        instance_type = config.default_instance_size
        tags = dict(Name=ResourceName)

        class provisioner:
            "file"
            source = "example.txt"
            destination = "/tmp/example.txt"

        class provisioner:
            "local-exec"
            command = f"echo Connecting to the DB ({db_module.db.public_ip})"

    class UbuntuMachineWest(UbuntuMachine):
        provider = AWS_West

    class TestModule(TFModule):
        source = "../tf_modules/test_module"
        service = Parameter("service")

    class MainServers(Module):
        east = [UbuntuMachine(i) for i in range(5)]
        west = UbuntuMachineWest()
        legacy_machine = UbuntuMachineUsingDeferred(db_module=db_module)
        TestModule(service="iam")

    Output("east_machine_arns", value=[server.arn for server in MainServers.east])
