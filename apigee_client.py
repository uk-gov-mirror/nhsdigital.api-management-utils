import requests
from functools import partialmethod


def raise_for_status_hook(response: requests.Response, *args, **kwargs):
    response.raise_for_status()


class ApigeeClient:
    def __init__(
        self,
        apigee_org: str,
        username: str = None,
        password: str = None,
        access_token: str = None,
        session: requests.Session = requests.Session,
    ):
        self.apigee_org = apigee_org

        if access_token:
            self.access_token = access_token
        elif username and password:
            self.access_token = self._get_access_token(username, password)

        self._session = session
        self._session.hooks = {"response": raise_for_status_hook}

    def _request(self, method: str, url: str, **kwargs):
        return self._session.request(
            method, url, headers=self._auth_headers, **kwargs
        )

    def get(self, url: str, **kwargs):
        return self._request("GET", url, **kwargs)

    post = partialmethod(_request, "POST")
    put = partialmethod(_request, "PUT")
    delete = partialmethod(_request, "DELETE")
    patch = partialmethod(_request, "PATCH")
    head = partialmethod(_request, "HEAD")
    options = partialmethod(_request, "OPTIONS")

    def list_specs(self):
        response = self.get(
            f"https://apigee.com/dapi/api/organizations/{self.apigee_org}/specs/folder/home"
        )
        return response.json()

    def create_spec(self, name: str, folder: str):
        response = self.post(
            f"https://apigee.com/dapi/api/organizations/{self.apigee_org}/specs/doc",
            json={"folder": folder, "name": name, "kind": "Doc"},
        )
        return response

    def update_spec(self, spec_id: str, content: str):
        response = self.put(
            f"https://apigee.com/dapi/api/organizations/{self.apigee_org}/specs/doc/{spec_id}/content",
            headers=dict(**{"Content-Type": "text/plain"}, **self._auth_headers),
            data=content.encode("utf-8"),
        )
        return response

    def get_portals(self):
        response = self.get(
            f"https://apigee.com/portals/api/sites?orgname={self.apigee_org}",
        )
        return response

    def get_apidocs(self, portal_id: str):
        response = self.get(
            f"https://apigee.com/portals/api/sites/{portal_id}/apidocs",
        )
        return response

    def create_portal_api(
        self,
        friendly_name: str,
        spec_name: str,
        spec_id: str,
        portal_id: str,
        visible: bool = True,
    ):
        response = self.post(
            f"https://apigee.com/portals/api/sites/{portal_id}/apidocs",
            json={
                "anonAllowed": True,
                "description": "",
                "edgeAPIProductName": spec_name,
                "requireCallbackUrl": True,
                "specContent": spec_id,
                "specId": spec_name,
                "title": friendly_name,
                "visibility": visible,
            },
        )
        return response

    def update_portal_api(
        self,
        apidoc_id: str,
        friendly_name: str,
        spec_name: str,
        spec_id: str,
        portal_id: str,
        visible: bool = True,
    ):
        response = self.put(
            f"https://apigee.com/portals/api/sites/{portal_id}/apidocs/{apidoc_id}",
            json={
                "anonAllowed": True,
                "description": "",
                "edgeAPIProductName": spec_name,
                "requireCallbackUrl": True,
                "specContent": spec_id,
                "specId": spec_name,
                "title": friendly_name,
                "visibility": visible,
            },
        )
        return response

    def get_apidoc(self, portal_id: str, apidoc_id: str):
        response = self.get(
            f"https://apigee.com/portals/api/sites/{portal_id}/apidocs/{apidoc_id}",
        )
        return response

    def update_spec_snapshot(self, portal_id: str, apidoc_id: str):
        apidoc = self.get_apidoc(portal_id, apidoc_id).json()["data"]

        self.put(
            f"https://apigee.com/portals/api/sites/{portal_id}/apidocs/{apidoc_id}",
            json={
                "anonAllowed": True,
                "description": apidoc["description"],
                "specId": apidoc["specId"],
                "visibility": True,
            },
        )

        return self.put(
            f"https://apigee.com/portals/api/sites/{portal_id}/apidocs/{apidoc_id}/snapshot",
        )

    def list_keystores(self, environment: str):
        response = self.get(
            f"https://api.enterprise.apigee.com/v1/organizations/{self.apigee_org}/environments/{environment}/keystores",
        )
        return response.json()

    def get_keystore(self, environment: str, keystore_name: str):
        response = self.get(
            f"https://api.enterprise.apigee.com/v1/organizations/{self.apigee_org}/environments/{environment}/keystores/{keystore_name}",
        )
        return response.json()

    def create_keystore(self, environment: str, keystore_name: str):
        """
        Create a return a keystore.

        Is idempotent, if keystore already exists will just retrieve.
        """
        if keystore_name in self.list_keystores(environment):
            return self.get_keystore(environment, keystore_name)

        response = self.post(
            f"https://api.enterprise.apigee.com/v1/organizations/{self.apigee_org}/environments/{environment}/keystores",
            data={"name": keystore_name},
        )

        return response.json()

    @property
    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def _get_access_token(self, username: str, password: str):
        response = self.post(
            "https://login.apigee.com/oauth/token",
            data={"username": username, "password": password, "grant_type": "password"},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0",
            },
        )
        return response.json()["access_token"]
