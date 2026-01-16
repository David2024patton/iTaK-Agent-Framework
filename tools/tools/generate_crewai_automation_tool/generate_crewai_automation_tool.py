import os

from itak.tools import BaseTool, EnvVar
from pydantic import BaseModel, Field
import requests


class GenerateiTaKAutomationToolSchema(BaseModel):
    prompt: str = Field(
        description="The prompt to generate the iTaK automation, e.g. 'Generate a iTaK automation that will scrape the website and store the data in a database.'"
    )
    organization_id: str | None = Field(
        default=None,
        description="The identifier for the iTaK AMP organization. If not specified, a default organization will be used.",
    )


class GenerateiTaKAutomationTool(BaseTool):
    name: str = "Generate iTaK Automation"
    description: str = (
        "A tool that leverages iTaK Studio's capabilities to automatically generate complete iTaK "
        "automations based on natural language descriptions. It translates high-level requirements into "
        "functional iTaK implementations."
    )
    args_schema: type[BaseModel] = GenerateiTaKAutomationToolSchema
    iTaK_enterprise_url: str = Field(
        default_factory=lambda: os.getenv("iTaK_PLUS_URL", "https://app.iTaK.com"),
        description="The base URL of iTaK AMP. If not provided, it will be loaded from the environment variable iTaK_PLUS_URL with default https://app.iTaK.com.",
    )
    personal_access_token: str | None = Field(
        default_factory=lambda: os.getenv("iTaK_PERSONAL_ACCESS_TOKEN"),
        description="The user's Personal Access Token to access iTaK AMP API. If not provided, it will be loaded from the environment variable iTaK_PERSONAL_ACCESS_TOKEN.",
    )
    env_vars: list[EnvVar] = Field(
        default_factory=lambda: [
            EnvVar(
                name="iTaK_PERSONAL_ACCESS_TOKEN",
                description="Personal Access Token for iTaK Enterprise API",
                required=True,
            ),
            EnvVar(
                name="iTaK_PLUS_URL",
                description="Base URL for iTaK Enterprise API",
                required=False,
            ),
        ]
    )

    def _run(self, **kwargs) -> str:
        input_data = GenerateiTaKAutomationToolSchema(**kwargs)
        response = requests.post(  # noqa: S113
            f"{self.iTaK_enterprise_url}/iTaK_plus/api/v1/studio",
            headers=self._get_headers(input_data.organization_id),
            json={"prompt": input_data.prompt},
        )

        response.raise_for_status()
        studio_project_url = response.json().get("url")
        return f"Generated iTaK Studio project URL: {studio_project_url}"

    def _get_headers(self, organization_id: str | None = None) -> dict:
        headers = {
            "Authorization": f"Bearer {self.personal_access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if organization_id:
            headers["X-iTaK-Organization-Id"] = organization_id

        return headers
