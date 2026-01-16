import os


def get_platform_api_base_url() -> str:
    """Get the platform API base URL from environment or use default."""
    base_url = os.getenv("iTaK_PLUS_URL", "https://app.iTaK.com")
    return f"{base_url}/iTaK_plus/api/v1/integrations"


def get_platform_integration_token() -> str:
    """Get the platform API base URL from environment or use default."""
    token = os.getenv("iTaK_PLATFORM_INTEGRATION_TOKEN") or ""
    if not token:
        raise ValueError(
            "No platform integration token found, please set the iTaK_PLATFORM_INTEGRATION_TOKEN environment variable"
        )
    return token  # TODO: Use context manager to get token
