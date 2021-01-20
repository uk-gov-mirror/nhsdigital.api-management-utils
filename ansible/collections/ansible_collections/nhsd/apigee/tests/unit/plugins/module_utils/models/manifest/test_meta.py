import uuid

import pytest
import pydantic

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.meta import (
    ManifestMetaApi,
)


def test_valid_api_name():
    ManifestMetaApi(name="canary-api", id=uuid.uuid4())


def test_api_name_with_numbers_invalid():
    with pytest.raises(pydantic.ValidationError):
        ManifestMetaApi(name="canary-api123", id=uuid.uuid4())


def test_api_name_with_underscores_invalid():
    with pytest.raises(pydantic.ValidationError):
        ManifestMetaApi(name="canary_api", id=uuid.uuid4())


def test_api_name_with_capitals_invalid():
    with pytest.raises(pydantic.ValidationError):
        ManifestMetaApi(name="Canary-Api", id=uuid.uuid4())
