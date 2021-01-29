import typing
import pydantic


class ApigeeProductAttribute(pydantic.BaseModel):
    name: pydantic.constr(regex=r"^(?!(access|ratelimit|api_guid|api_spec_guid)$)")
    value: str


class ApigeeProductAttributeAccess(pydantic.BaseModel):
    name: typing.Literal["access"]
    value: typing.Literal["public", "private"]


class ApigeeProductAttributeRateLimit(pydantic.BaseModel):
    name: typing.Literal["ratelimit"]
    value: pydantic.constr(regex=r"^[0-9]+(ps|pm)$")


class StringValueMixin:
    """Convert a non-string value attribute to string on export."""

    def dict(self, **kwargs):
        native = super().dict(**kwargs)
        native.update({"value": str(native["value"])})
        return native


class ApigeeProductAttributeApiSpecGuid(StringValueMixin, pydantic.BaseModel):
    name: typing.Literal["api_spec_guid"]
    value: pydantic.UUID4


class ApigeeProductAttributeApiGuid(StringValueMixin, pydantic.BaseModel):
    name: typing.Literal["api_guid"]
    value: pydantic.UUID4


class ApigeeProduct(pydantic.BaseModel):
    name: str
    approvalType: typing.Literal["auto", "manual"]
    attributes: typing.List[
            typing.Union[
                ApigeeProductAttributeAccess,
                ApigeeProductAttributeRateLimit,
                ApigeeProductAttributeApiSpecGuid,
                ApigeeProductAttributeApiGuid,
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
