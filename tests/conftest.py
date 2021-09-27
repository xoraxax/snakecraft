import pytest

from snakecraft.core import model, reset_model


@pytest.fixture
def get_tf_object():
    yield lambda: model.as_object
    reset_model()
