import pytest
import apigee_client
from unittest.mock import Mock


@pytest.fixture
def client():
    fake_session = Mock()

    return apigee_client.ApigeeClient(
        apigee_org="test", access_token="test", session=fake_session
    )


def test_get(client):
    client.get("https://test.com")

    client._session.request.assert_called_with(
        "GET", "https://test.com", headers={"Authorization": "Bearer test"}
    )


def test_list_specs(client):
    client.list_specs()

    client._session.request.assert_called_with(
        "GET",
        "https://apigee.com/dapi/api/organizations/test/specs/folder/home",
        headers={"Authorization": "Bearer test"},
    )
