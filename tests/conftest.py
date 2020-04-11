import pytest

from app.resource import Resource


@pytest.fixture(name="resource")
def fixture_resource():
    return Resource()
