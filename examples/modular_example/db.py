from snakecraft import Module, Parameter, ResourceName

from .providers import AWS


class DatabaseAMI(AWS.Data.ami):
    most_recent = True

    class filter:
        name = "name"
        values = ["RDMS-Database 3000-v1.*"]


def make_db_module(config, ubuntu_ami):
    class DatabaseMachine(AWS.Resource.instance):
        ami = DatabaseAMI()
        instance_type = config.default_instance_size
        tags = dict(Name=ResourceName)

    class MonitorServer(AWS.Resource.instance):
        ami = ubuntu_ami
        instance_type = "t3.micro"
        tags = {
            "db": Parameter("db").hostname,
        }

    class DBModule(Module):
        db = DatabaseMachine()
        monitor = MonitorServer("monitor", db=db)

    return DBModule
