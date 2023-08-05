from myst.client import Client
from myst.openapi.models.model_fit_job_get import ModelFitJobGet


def request_sync(client: Client, project_uuid: str, model_uuid: str, uuid: str) -> ModelFitJobGet:
    """Get a fit job for model."""

    return client.request(
        method="get",
        path=f"/projects/{project_uuid}/models/{model_uuid}/fit_jobs/{uuid}",
        response_class=ModelFitJobGet,
    )
