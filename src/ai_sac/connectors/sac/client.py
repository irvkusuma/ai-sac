
import os

import httpx

from ai_sac.connectors.sac.auth import get_access_token


class SacApiError(Exception):
    """Raised when a SAC Data Export API request fails."""


def get_providers() -> list[dict]:
    """
    Retrieve available Planning Model providers
    from the SAC Data Export Service.
    """

    tenant_url = os.getenv("SAC_TENANT_URL")

    if not tenant_url:
        raise SacApiError("SAC_TENANT_URL is missing.")

    base_url = (
        f"{tenant_url.rstrip('/')}/api/v1/dataexport"
    )

    endpoint = (
        "/administration/"
        "Namespaces(NamespaceID='sac')/Providers"
    )

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "x-sap-sac-custom-auth": "true",
        "Accept": "application/json",
    }

    try:
        response = httpx.get(
            f"{base_url}{endpoint}",
            headers=headers,
            timeout=60.0,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("value", [])

    except httpx.HTTPStatusError as exc:
        raise SacApiError(
            f"SAC Data Export API returned HTTP "
            f"{exc.response.status_code}: {exc.response.text}"
        ) from exc

    except httpx.RequestError as exc:
        raise SacApiError(
            f"Could not connect to SAC Data Export API: {exc}"
        ) from exc

    except ValueError as exc:
        raise SacApiError(
            "SAC Data Export API returned invalid JSON."
        ) from exc


def _get_provider_url() -> str:
    tenant_url = os.getenv("SAC_TENANT_URL")
    provider_id = os.getenv("SAC_PROVIDER_ID")

    if not tenant_url:
        raise SacApiError("SAC_TENANT_URL is missing.")

    if not provider_id:
        raise SacApiError("SAC_PROVIDER_ID is missing.")

    return (
        f"{tenant_url.rstrip('/')}"
        f"/api/v1/dataexport/providers/sac/{provider_id}"
    )


def get_provider_service_document() -> dict:
    """Retrieve available entity sets for the target provider."""

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "x-sap-sac-custom-auth": "true",
        "Accept": "application/json",
    }

    try:
        response = httpx.get(
            f"{_get_provider_url()}/",
            headers=headers,
            timeout=60.0,
        )

        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as exc:
        raise SacApiError(
            f"Service document failed: HTTP "
            f"{exc.response.status_code}: {exc.response.text}"
        ) from exc

    except httpx.RequestError as exc:
        raise SacApiError(
            f"Service document connection failed: {exc}"
        ) from exc


def get_provider_metadata() -> str:
    """Retrieve OData metadata XML for the target provider."""

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "x-sap-sac-custom-auth": "true",
        "Accept": "application/xml",
    }

    try:
        response = httpx.get(
            f"{_get_provider_url()}/$metadata",
            headers=headers,
            timeout=60.0,
        )

        response.raise_for_status()
        return response.text

    except httpx.HTTPStatusError as exc:
        raise SacApiError(
            f"Metadata request failed: HTTP "
            f"{exc.response.status_code}: {exc.response.text}"
        ) from exc

    except httpx.RequestError as exc:
        raise SacApiError(
            f"Metadata connection failed: {exc}"
        ) from exc


def get_fact_data(
    params: dict | None = None,
    max_pages: int = 1000,
) -> dict:
    """
    Extract FactData from SAC Data Export Service.

    Returns records and extraction status.
    """
    if max_pages < 1:
        raise ValueError("max_pages must be at least 1.")

    url = f"{_get_provider_url()}/FactData"
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "x-sap-sac-custom-auth": "true",
        "Accept": "application/json",
    }

    records = []
    pages_fetched = 0
    next_url = url
    request_params = params or {}

    try:
        with httpx.Client(
            headers=headers,
            timeout=120.0,
        ) as client:

            while next_url and pages_fetched < max_pages:
                response = client.get(
                    next_url,
                    params=(
                        request_params
                        if pages_fetched == 0
                        else None
                    ),
                )
                response.raise_for_status()

                data = response.json()

                if "value" not in data:
                    raise SacApiError(
                        "FactData response does not contain 'value'."
                    )

                records.extend(data["value"])
                pages_fetched += 1
                next_url = data.get("@odata.nextLink")

        return {
            "records": records,
            "pages_fetched": pages_fetched,
            "has_more_data": next_url is not None,
            "is_complete": next_url is None,
        }

    except httpx.HTTPStatusError as exc:
        raise SacApiError(
            f"FactData extraction failed. HTTP "
            f"{exc.response.status_code}: {exc.response.text}"
        ) from exc

    except httpx.RequestError as exc:
        raise SacApiError(
            f"FactData connection failed: {exc}"
        ) from exc

    except ValueError as exc:
        raise SacApiError(
            "FactData returned invalid JSON."
        ) from exc
