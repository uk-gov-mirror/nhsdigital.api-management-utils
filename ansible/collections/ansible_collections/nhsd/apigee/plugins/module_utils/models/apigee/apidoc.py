import pydantic


class ApigeeApidoc(pydantic.BaseModel):
    edgeAPIProductName: str
    anonAllowed: bool
    description: str
    requireCallbackUrl: bool
    title: str
    visibility: bool
    specId: str = ""
    specContent: str = ""
