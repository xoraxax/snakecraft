from snakecraft import Config

from .cluster import make_cluster
from .prod import config as prod_config
from .test import config as test_config

env_config = prod_config if Config.env == "prod" else test_config


def run():
    make_cluster(env_config.Config)
