from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    year: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/draft/{year}/latest".format(
            year=quote(str(year), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == 200:
        return None

    if response.status_code == 401:
        return None

    if response.status_code == 403:
        return None

    if response.status_code == 404:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    year: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    """View latest player drafted, endpoint best used when draft is currently open.


    **Description:**
    This endpoint returns biographical and financial data for the most recent pick in the Rule 4 draft.

    **Return Includes:** Player name, id, financial data, & team data.

    **Required Parameters:** year is required to run this call.

    ---
    **Example of call with required parameters:**

    https://statsapi.mlb.com/api/v1/draft/2018/latest

    Args:
        year (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        year=year,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    year: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any]:
    """View latest player drafted, endpoint best used when draft is currently open.


    **Description:**
    This endpoint returns biographical and financial data for the most recent pick in the Rule 4 draft.

    **Return Includes:** Player name, id, financial data, & team data.

    **Required Parameters:** year is required to run this call.

    ---
    **Example of call with required parameters:**

    https://statsapi.mlb.com/api/v1/draft/2018/latest

    Args:
        year (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        year=year,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
