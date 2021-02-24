import typing

APIGEE_BASE_URL = "https://api.enterprise.apigee.com/v1/"
APIGEE_DAPI_URL = "https://apigee.com/dapi/api/"

APIGEE_ORG_TO_ENV = {
    "nhsd-nonprod": [
        "internal-dev",
        "internal-dev-sandbox",
        "internal-qa",
        "internal-qa-sandbox",
        "ref",
    ],
    "nhsd-prod": ["dev", "int", "sandbox", "prod"],
}

# Maps unique API IDS to API names and Spec guids.  One day this will
# be a proper microservice. But for now, this will do.
REGISTERED_META = [
    {
        "guid": "96836235-09a5-4064-9220-0812765ebdd7",
        "name": "canary-api",
        "spec_guids": ["0af08cfb-6835-47b5-867c-95d41ef849b5"],
    },
    {
        "guid": "b3d5c83f-98f2-429c-ba1d-646dccd139a3",
        "name": "hello-world",
        "spec_guids": ["e8663c19-725f-4883-b272-a9da868d5541"],
    },
    {
        "guid": "a3213966-9b13-400c-8fdd-e239e56a2742",
        "name": "mesh-api-specification",
        "spec_guids": ["73a3d6dd-912b-4793-bf4c-bf80c4bc34d1"],
    },
    {
        "guid": "eef32850-52ae-46da-9dbd-d9f3df818846",
        "name": "personal-demographics",
        "spec_guids": ["a343a204-f2d2-4287-a2e5-b5cb367e35bb"],
    },
    {
        "guid": "9c644a26-c926-4fae-9564-5a9c49ab332d",
        "name": "electronic-prescription-service-api",
        "spec_guids": ["5ead5713-9d2b-46eb-8626-def5fd2a2350"],
    },
    {
        "guid": "13cfc3dd-38c3-4692-9cfb-50d540e8cfe3",
        "name": "reasonable-adjustment-flag",
        "spec_guids": ["9f2d5659-ef7d-4815-ac25-d11f4ce75c25"],
    },
    {
        "guid": "090e12f4-6f3c-4ea7-b7eb-d70687d22cea",
        "name": "ambulance-analytics",
        "spec_guids": ["538699e8-d039-4473-9e35-e3b79eb92d1e"],
    },
    {
        "guid": "fa1c780f-6fb6-4c8e-a73c-eb2c306ca4f1",
        "name": "spine-directory-service",
        "spec_guids": ["88a3ec29-7ab1-4ac4-ae32-e367767b3ed8"],
    },
    {
        "guid": "7541eb6b-3416-4aee-bd66-8766c1f90cfb",
        "name": "nhs-app",
        "spec_guids": ["f5b9779e-d343-4a0a-8410-6dcae48bc55e"],
    },
    # {
    #     "guid": "b26b0249-488d-44f9-93ed-9d2f08f3859c",
    #     "name": "signing-service-api",
    #     "spec_guids": ["a062e39c-b843-4833-8d24-8fc1434900a0",],
    # },
    {
        "guid": "3ef873d7-18d3-4c51-b1f4-d36a3749c857",
        "name": "summary-care-record",
        "spec_guids": ["bec2d100-b515-4fa6-8a2f-617d73182b83"],
    },
    {
        "guid": "343026de-b0f5-4c45-a53e-3a1b687bab9d",
        "name": "e-referrals-service-api",
        "spec_guids": ["2ff6fce6-8b51-4d88-a528-4fd1edd18541"],
    },
    {
        "guid": "d5a3f4fc-e61f-41f3-ab72-16aa5ef3ff2b",
        "name": "identity-service",
        "spec_guids": [],
    },
    {
        "guid": "f61f73c1-2c9f-4f0c-b047-ab1464f867fc",
        "name": "async-slowapp",
        "spec_guids": [],
    },
    {
        "guid": "5d47b3a7-711e-4a2f-9db8-0e9dd06df24f",
        "name": "sync-wrap",
        "spec_guids": [],
    },
    {
        "guid": "d85314fc-9951-491c-95b1-debd819c9f3f",
        "name": "monitoring-service-discovery",
        "spec_guids": [],
    },
    {
        "guid": "9f11c568-4447-4a27-ad02-d67a846b8d59",
        "name": "risk-stratification",
        "spec_guids": ["36823b1f-bcba-4335-8fd6-f3e06a21f3db"],
    },
    {
        "guid": "7c2bcb03-c552-43d3-b5d7-757387453103",
        "name": "slackbot",
        "spec_guids": [],
    },
]

def portal_uri(org: typing.Literal["nhsd-nonprod", "nhsd-prod"]) -> str:
    portal_ids = {
        "nhsd-nonprod": "nhsd-nonprod-developerportal",
        "nhsd-prod": "nhsd-prod-developerportal",
    }
    if org not in portal_ids:
        raise ValueError(f"Invalid organization name {org}")
    return f"https://apigee.com/portals/api/sites/{portal_ids[org]}/apidocs"



