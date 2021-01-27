import typing
import pydantic


class ApigeeProductAttribute(pydantic.BaseModel):
    name: pydantic.constr(regex=r"^(?!(access|ratelimit|spec_guid)$)")
    value: str


class ApigeeProductAttributeAccess(ApigeeProductAttribute):
    name: typing.Literal["access"]
    value: typing.Literal["public", "private"]


class ApigeeProductAttributeRateLimit(ApigeeProductAttribute):
    name: typing.Literal["ratelimit"]
    value: pydantic.constr(regex=r"^[0-9]+(ps|pm)$")


class ApigeeProductAttributeSpecGuid(ApigeeProductAttribute):
    name: typing.Literal["spec_guid"]
    value: pydantic.UUID4

    def dict(self, **kwargs):
        native = super().dict(**kwargs)
        native.update({"value": str(native["value"])})
        return native


class ApigeeProduct(pydantic.BaseModel):
    name: str
    approvalType: typing.Literal["auto", "manual"]
    attributes: typing.List[
            typing.Union[
                ApigeeProductAttributeAccess,
                ApigeeProductAttributeRateLimit,
                ApigeeProductAttributeSpecGuid,
                ApigeeProductAttribute,
            ],
        ]
    description: str
    displayName: str
    environments: typing.List[str]
    proxies: typing.List[str]
    quota: str
    quotaInterval: str
    quotaTimeUnit: typing.Literal["minute", "hour"]
    scopes: typing.List[str]

    @pydantic.validator("attributes")
    def validate_attributes(cls, attributes, values):
        for required_name in ["access", "ratelimit"]:
            attrs = [a for a in attributes if a.name == required_name]
            if len(attrs) != 1:
                raise AssertionError(
                    f"Product {values['name']} must contain exactly 1 attribute with name: '{required_name}', found {len(attrs)}"
                )
        return attributes
