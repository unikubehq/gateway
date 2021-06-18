from gql import Client
from gql.transport.requests import RequestsHTTPTransport

import settings


def get_transportation(url: str, token: str = None) -> RequestsHTTPTransport:
    return RequestsHTTPTransport(
        url=url,
        use_json=True,
        headers={
            "Content-type": "application/json",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
        verify=False,
        timeout=settings.GQL_TIMEOUT,
    )


def get_client(url: str, token: str = None) -> Client:
    client = Client(
        transport=get_transportation(url, token),
        fetch_schema_from_transport=True,
    )
    return client
