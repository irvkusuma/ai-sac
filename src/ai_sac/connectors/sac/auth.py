
import os

import httpx


class SacAuthError(Exception):
    """Raised when SAC OAuth authentication fails."""


def get_access_token() -> str:
    """
    Request an OAuth access token from SAP Analytics Cloud
    using the Client Credentials grant.
    """

    token_url = os.getenv("SAC_TOKEN_URL")
    client_id = os.getenv("SAC_CLIENT_ID")
    client_secret = os.getenv("SAC_CLIENT_SECRET")

    # Validate environment variables
    missing = [
        name
        for name, value in {
            "SAC_TOKEN_URL": token_url,
            "SAC_CLIENT_ID": client_id,
            "SAC_CLIENT_SECRET": client_secret,
        }.items()
        if not value
    ]

    if missing:
        raise SacAuthError(
            f"Missing environment variables: {', '.join(missing)}"
        )

    try:
        response = httpx.post(
            token_url,
            params={"grant_type": "client_credentials"},
            auth=(client_id, client_secret),
            headers={"Accept": "application/json"},
            timeout=30.0,
        )

        response.raise_for_status()

        token_data = response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise SacAuthError(
                "OAuth response does not contain access_token."
            )

        return access_token

    except httpx.HTTPStatusError as exc:
        raise SacAuthError(
            f"SAC OAuth rejected the request. "
            f"HTTP {exc.response.status_code}: {exc.response.text}"
        ) from exc

    except httpx.RequestError as exc:
        raise SacAuthError(
            f"Could not connect to SAC OAuth endpoint: {exc}"
        ) from exc

    except ValueError as exc:
        raise SacAuthError(
            "SAC OAuth returned an invalid JSON response."
        ) from exc
