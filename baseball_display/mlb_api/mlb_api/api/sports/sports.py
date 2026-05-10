from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sports_rest_object import SportsRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    sport_id: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_sport_id: list[str] | Unset = UNSET
    if not isinstance(sport_id, Unset):
        json_sport_id = sport_id

    params["sportId"] = json_sport_id

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sports",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | SportsRestObject | None:
    if response.status_code == 200:
        response_200 = SportsRestObject.from_dict(response.json())

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
) -> Response[Any | SportsRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    sport_id: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | SportsRestObject]:
    """View information for all sportIds.

     **Description:**
     This endpoint returns information for all sports available via the Stats API

     **Return Includes:** SportId and sport name.

     **Required Parameters:** No parameters are required to run this call.


    Args:
        sport_id (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SportsRestObject]
    """

    kwargs = _get_kwargs(
        sport_id=sport_id,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    sport_id: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | SportsRestObject | None:
    """View information for all sportIds.

     **Description:**
     This endpoint returns information for all sports available via the Stats API

     **Return Includes:** SportId and sport name.

     **Required Parameters:** No parameters are required to run this call.


    Args:
        sport_id (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | SportsRestObject
    """

    return sync_detailed(
        client=client,
        sport_id=sport_id,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    sport_id: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | SportsRestObject]:
    """View information for all sportIds.

     **Description:**
     This endpoint returns information for all sports available via the Stats API

     **Return Includes:** SportId and sport name.

     **Required Parameters:** No parameters are required to run this call.


    Args:
        sport_id (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | SportsRestObject]
    """

    kwargs = _get_kwargs(
        sport_id=sport_id,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    sport_id: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | SportsRestObject | None:
    """View information for all sportIds.

     **Description:**
     This endpoint returns information for all sports available via the Stats API

     **Return Includes:** SportId and sport name.

     **Required Parameters:** No parameters are required to run this call.


    Args:
        sport_id (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | SportsRestObject
    """

    return (
        await asyncio_detailed(
            client=client,
            sport_id=sport_id,
            fields=fields,
        )
    ).parsed
