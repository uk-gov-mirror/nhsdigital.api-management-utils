import typing
import re

import pydantic


class ApigeeProductAttribute(pydantic.BaseModel):
    name: str
    value: str

    @pydantic.validator("value")
    def validate_special_attribute(cls, value, values):
        name = values.get("name")
        if name == "access" and value not in ["public", "private"]:
            raise ValueError(f"Product attribute 'access' must be 'public' or 'private', not {value}")
        if name == "ratelimit" and not re.match(r"^[0-9]+(ps|pm)$", value):
            raise ValueError(
                f"Product attribute ratelimit must be an integer followed ps or pm, e.g. '300ps', not {value}"
            )
        return value


def assert_attribute(name, attributes):
    if len([a for a in attributes if a.name == name]) != 1:
        raise AssertionError(
            f"All products must contain exactly 1 attribute named '{name}'"
        )


class ApigeeProduct(pydantic.BaseModel):
    approvalType: typing.Literal["auto", "manual"]
    attributes: typing.List[ApigeeProductAttribute]
    description: str
    displayName: str
    environments: typing.List[str]
    name: str
    proxies: typing.List[str]
    quota: str
    quotaInterval: str
    quotaTimeUnit: typing.Literal["minute", "hour"]
    scopes: typing.List[str]

    @pydantic.validator("attributes")
    def validate_attributes(cls, attributes):
        assert_attribute("access", attributes)
        assert_attribute("ratelimit", attributes)
        return attributes
