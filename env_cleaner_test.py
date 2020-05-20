import pytest
import env_cleaner
from unittest.mock import Mock, call


def list_specs_response():
    return {
        "contents": [
            {"name": "personal-demographics"},
            {"name": "personal-demographics-test"},
        ]
    }


def list_proxies_response():
    return [
        "personal-demographics-internal-dev",
        "personal-demographics-internal-dev-test",
        "personal-demographics-internal-dev-test-sandbox",
    ]


def list_products_response():
    return list_proxies_response()  # Left intentionally because they usually match up


def get_proxy_response(proxy):
    return {"revision": ["1"]}


@pytest.fixture
def client():
    class FakeApigeeClient:
        list_specs = Mock()
        list_specs.side_effect = list_specs_response
        list_proxies = Mock()
        list_proxies.side_effect = list_proxies_response
        list_products = Mock()
        list_products.side_effect = list_products_response
        get_proxy = Mock()
        get_proxy.side_effect = get_proxy_response
        undeploy_proxy_revision = Mock()
        delete_proxy = Mock()
        delete_spec = Mock()
        delete_product = Mock()

    return FakeApigeeClient()


def test_clean_everything(client):
    env_cleaner.clean_env(
        client,
        "test_env",
        should_clean_specs=True,
        should_clean_proxies=True,
        should_clean_products=True,
        sandboxes_only=False,
        dry_run=False,
        undeploy_only=False,
    )

    client.list_specs.assert_called()
    client.list_proxies.assert_called()
    client.list_products.assert_called()

    client.get_proxy.assert_has_calls(
        [
            call("personal-demographics-internal-dev-test"),
            call("personal-demographics-internal-dev-test-sandbox"),
        ]
    )

    client.delete_spec.assert_called_with("personal-demographics-test")
    client.undeploy_proxy_revision.assert_has_calls(
        [
            call("test_env", "personal-demographics-internal-dev-test", "1"),
            call("test_env", "personal-demographics-internal-dev-test-sandbox", "1"),
        ]
    )
    client.delete_proxy.assert_has_calls(
        [
            call("personal-demographics-internal-dev-test"),
            call("personal-demographics-internal-dev-test-sandbox"),
        ]
    )
    client.delete_product.assert_has_calls(
        [
            call("personal-demographics-internal-dev-test"),
            call("personal-demographics-internal-dev-test-sandbox"),
        ]
    )


def test_proxy_dry_run(client):
    env_cleaner.clean_env(client, "test_env", should_clean_proxies=True, dry_run=True)

    client.list_proxies.assert_called()
    client.get_proxy.assert_has_calls(
        [
            call("personal-demographics-internal-dev-test"),
            call("personal-demographics-internal-dev-test-sandbox"),
        ]
    )
    client.undeploy_proxy_revision.assert_not_called()
    client.delete_proxy.assert_not_called()


def test_proxy_sandboxes_only(client):
    env_cleaner.clean_env(
        client, "test_env", should_clean_proxies=True, sandboxes_only=True
    )

    client.list_proxies.assert_called()
    client.get_proxy.assert_has_calls(
        [
            call("personal-demographics-internal-dev-test-sandbox")
        ]
    )
    client.undeploy_proxy_revision.assert_has_calls(
        [call("test_env", "personal-demographics-internal-dev-test-sandbox", "1"),]
    )
    client.delete_proxy.assert_has_calls(
        [call("personal-demographics-internal-dev-test-sandbox")]
    )


def test_proxy_undeploy_only(client):
    env_cleaner.clean_env(
        client, "test_env", should_clean_proxies=True, undeploy_only=True
    )

    client.list_proxies.assert_called()
    client.get_proxy.assert_has_calls(
        [
            call("personal-demographics-internal-dev-test"),
            call("personal-demographics-internal-dev-test-sandbox"),
        ]
    )
    client.undeploy_proxy_revision.assert_has_calls(
        [
            call("test_env", "personal-demographics-internal-dev-test", "1"),
            call("test_env", "personal-demographics-internal-dev-test-sandbox", "1"),
        ]
    )
    client.delete_proxy.assert_not_called()
