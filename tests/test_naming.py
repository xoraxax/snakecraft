import pytest

from snakecraft import Provider
from snakecraft.exceptions import DuplicateDeclarationException

provider = Provider("does_not_exist")


def test_duplicate_class_name(get_tf_object):
    class Instance(provider.Resource.instance):
        pass

    Instance0 = Instance

    class Instance(provider.Resource.instance):
        pass

    with pytest.raises(DuplicateDeclarationException):
        Instance0(), Instance()
        get_tf_object()


def test_international_name(get_tf_object):
    class Instance(provider.Resource.instance):
        name = "Naïve"

    Instance()
    get_tf_object()
