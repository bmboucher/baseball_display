from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/scheduleEventTypes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list[Any] | None:
    if response.status_code == 200:
        response_200 = cast(list[Any], response.json())

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | list[Any]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | list[Any]]:
    """Scheduled event types


    **Description:**
    This endpoint returns all scheduled event types available on the Stats API.

    **Return Includes:** scheduleEventTypes.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/scheduleEventTypes

    Args:
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[Any]]
    """

    kwargs = _get_kwargs(
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Any | list[Any] | None:
    """Scheduled event types


    **Description:**
    This endpoint returns all scheduled event types available on the Stats API.

    **Return Includes:** scheduleEventTypes.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/scheduleEventTypes

    Args:
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[Any]
    """

    return sync_detailed(
        client=client,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | list[Any]]:
    """Scheduled event types


    **Description:**
    This endpoint returns all scheduled event types available on the Stats API.

    **Return Includes:** scheduleEventTypes.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/scheduleEventTypes

    Args:
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[Any]]
    """

    kwargs = _get_kwargs(
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Any | list[Any] | None:
    """Scheduled event types


    **Description:**
    This endpoint returns all scheduled event types available on the Stats API.

    **Return Includes:** scheduleEventTypes.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/scheduleEventTypes

    Args:
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[Any]
    """

    return (
        await asyncio_detailed(
            client=client,
            fields=fields,
        )
    ).parsed
