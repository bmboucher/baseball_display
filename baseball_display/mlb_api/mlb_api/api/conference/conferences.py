from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.conferences_rest_object import ConferencesRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    conference_id: int,
    *,
    season: list[int] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_season: list[int] | Unset = UNSET
    if not isinstance(season, Unset):
        json_season = season

    params["season"] = json_season

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/conferences/{conference_id}".format(
            conference_id=quote(str(conference_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ConferencesRestObject | None:
    if response.status_code == 200:
        response_200 = ConferencesRestObject.from_dict(response.json())

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
) -> Response[Any | ConferencesRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    conference_id: int,
    *,
    client: AuthenticatedClient | Client,
    season: list[int] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | ConferencesRestObject]:
    """View PCL conferences by conferenceId.


    **Description:**
    This endpoint returns all information  on PCL conferences available on the Stats API.

    **Return Includes:** Conference name and league name.

    **Required Parameters:** conferenceId is required to run this call.

    ---
    **Example of call with all parameters:**
    https://statsapi.mlb.com/api/v1/conferences/302?season=2018

    Args:
        conference_id (int):
        season (list[int] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ConferencesRestObject]
    """

    kwargs = _get_kwargs(
        conference_id=conference_id,
        season=season,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    conference_id: int,
    *,
    client: AuthenticatedClient | Client,
    season: list[int] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | ConferencesRestObject | None:
    """View PCL conferences by conferenceId.


    **Description:**
    This endpoint returns all information  on PCL conferences available on the Stats API.

    **Return Includes:** Conference name and league name.

    **Required Parameters:** conferenceId is required to run this call.

    ---
    **Example of call with all parameters:**
    https://statsapi.mlb.com/api/v1/conferences/302?season=2018

    Args:
        conference_id (int):
        season (list[int] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ConferencesRestObject
    """

    return sync_detailed(
        conference_id=conference_id,
        client=client,
        season=season,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    conference_id: int,
    *,
    client: AuthenticatedClient | Client,
    season: list[int] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | ConferencesRestObject]:
    """View PCL conferences by conferenceId.


    **Description:**
    This endpoint returns all information  on PCL conferences available on the Stats API.

    **Return Includes:** Conference name and league name.

    **Required Parameters:** conferenceId is required to run this call.

    ---
    **Example of call with all parameters:**
    https://statsapi.mlb.com/api/v1/conferences/302?season=2018

    Args:
        conference_id (int):
        season (list[int] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ConferencesRestObject]
    """

    kwargs = _get_kwargs(
        conference_id=conference_id,
        season=season,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    conference_id: int,
    *,
    client: AuthenticatedClient | Client,
    season: list[int] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | ConferencesRestObject | None:
    """View PCL conferences by conferenceId.


    **Description:**
    This endpoint returns all information  on PCL conferences available on the Stats API.

    **Return Includes:** Conference name and league name.

    **Required Parameters:** conferenceId is required to run this call.

    ---
    **Example of call with all parameters:**
    https://statsapi.mlb.com/api/v1/conferences/302?season=2018

    Args:
        conference_id (int):
        season (list[int] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ConferencesRestObject
    """

    return (
        await asyncio_detailed(
            conference_id=conference_id,
            client=client,
            season=season,
            fields=fields,
        )
    ).parsed
