import pydantic


class AddPolicyToPreFlow(pydantic.BaseModel):
    dist_dir: pydantic.DirectoryPath = ""
    proxy_dir: str
    policy_name: str

    @pydantic.validator("proxy_dir")
    def check_exists(cls, proxy_dir, values):
        dist_dir = values.get("dist_dir")
        if not dist_dir:  # Already errored
            return proxy_dir
        full_proxy_path = dist_dir.joinpath(f"proxies/{proxy_dir}")
        if not full_proxy_path.exists():
            raise ValueError(
                f"Full path to proxy_dir {str(full_proxy_path)} does not exist"
            )
        return proxy_dir

    def dict(self, **kwargs):
        native = super().dict(**kwargs)
        native.update(
            {
                "dist_dir": str(native["dist_dir"]),
            }
        )
        return native
