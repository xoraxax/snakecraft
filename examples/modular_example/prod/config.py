from ..config import MyProjectConfig


class Config(MyProjectConfig):
    env = "prod"
    default_instance_size = "t3.xlarge"
