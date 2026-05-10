from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.play_by_play_rest_object import PlayByPlayRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    game_mode_id: int | Unset = UNSET,
    timecode: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    is_non_statcast: bool | Unset = UNSET,
    offset: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["gameModeId"] = game_mode_id

    params["timecode"] = timecode

    params["limit"] = limit

    params["sortBy"] = sort_by

    params["isNonStatcast"] = is_non_statcast

    params["offset"] = offset

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/game/analytics/game",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | PlayByPlayRestObject | None:
    if response.status_code == 200:
        response_200 = PlayByPlayRestObject.from_dict(response.json())

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
) -> Response[Any | PlayByPlayRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    game_mode_id: int | Unset = UNSET,
    timecode: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    is_non_statcast: bool | Unset = UNSET,
    offset: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | PlayByPlayRestObject]:
    """View timestamps of most recent data corrections made to games.

     **Description:**
    This endpoint returns timestamps reflecting the most recent data corrections made to Games.

    **Return Includes:** timestamps.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with required parameters**

    http://statsapi.mlb.com/api/v1/analytics/game

    ---

    **Example of call with all parameters**

    http://statsapi.mlb.com/api/v1/analytics/game?lastMetricsUpdatedTime=2019-01-
    04T00:00:00.007380Z&gameModeId=2&sortBy=lastMetricsUpdatedTime&limit=1

    Args:
        game_mode_id (int | Unset):
        timecode (str | Unset):
        limit (str | Unset):
        sort_by (str | Unset):
        is_non_statcast (bool | Unset):
        offset (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PlayByPlayRestObject]
    """

    kwargs = _get_kwargs(
        game_mode_id=game_mode_id,
        timecode=timecode,
        limit=limit,
        sort_by=sort_by,
        is_non_statcast=is_non_statcast,
        offset=offset,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    game_mode_id: int | Unset = UNSET,
    timecode: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    is_non_statcast: bool | Unset = UNSET,
    offset: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | PlayByPlayRestObject | None:
    """View timestamps of most recent data corrections made to games.

     **Description:**
    This endpoint returns timestamps reflecting the most recent data corrections made to Games.

    **Return Includes:** timestamps.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with required parameters**

    http://statsapi.mlb.com/api/v1/analytics/game

    ---

    **Example of call with all parameters**

    http://statsapi.mlb.com/api/v1/analytics/game?lastMetricsUpdatedTime=2019-01-
    04T00:00:00.007380Z&gameModeId=2&sortBy=lastMetricsUpdatedTime&limit=1

    Args:
        game_mode_id (int | Unset):
        timecode (str | Unset):
        limit (str | Unset):
        sort_by (str | Unset):
        is_non_statcast (bool | Unset):
        offset (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PlayByPlayRestObject
    """

    return sync_detailed(
        client=client,
        game_mode_id=game_mode_id,
        timecode=timecode,
        limit=limit,
        sort_by=sort_by,
        is_non_statcast=is_non_statcast,
        offset=offset,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    game_mode_id: int | Unset = UNSET,
    timecode: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    is_non_statcast: bool | Unset = UNSET,
    offset: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | PlayByPlayRestObject]:
    """View timestamps of most recent data corrections made to games.

     **Description:**
    This endpoint returns timestamps reflecting the most recent data corrections made to Games.

    **Return Includes:** timestamps.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with required parameters**

    http://statsapi.mlb.com/api/v1/analytics/game

    ---

    **Example of call with all parameters**

    http://statsapi.mlb.com/api/v1/analytics/game?lastMetricsUpdatedTime=2019-01-
    04T00:00:00.007380Z&gameModeId=2&sortBy=lastMetricsUpdatedTime&limit=1

    Args:
        game_mode_id (int | Unset):
        timecode (str | Unset):
        limit (str | Unset):
        sort_by (str | Unset):
        is_non_statcast (bool | Unset):
        offset (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PlayByPlayRestObject]
    """

    kwargs = _get_kwargs(
        game_mode_id=game_mode_id,
        timecode=timecode,
        limit=limit,
        sort_by=sort_by,
        is_non_statcast=is_non_statcast,
        offset=offset,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    game_mode_id: int | Unset = UNSET,
    timecode: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    is_non_statcast: bool | Unset = UNSET,
    offset: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | PlayByPlayRestObject | None:
    """View timestamps of most recent data corrections made to games.

     **Description:**
    This endpoint returns timestamps reflecting the most recent data corrections made to Games.

    **Return Includes:** timestamps.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with required parameters**

    http://statsapi.mlb.com/api/v1/analytics/game

    ---

    **Example of call with all parameters**

    http://statsapi.mlb.com/api/v1/analytics/game?lastMetricsUpdatedTime=2019-01-
    04T00:00:00.007380Z&gameModeId=2&sortBy=lastMetricsUpdatedTime&limit=1

    Args:
        game_mode_id (int | Unset):
        timecode (str | Unset):
        limit (str | Unset):
        sort_by (str | Unset):
        is_non_statcast (bool | Unset):
        offset (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PlayByPlayRestObject
    """

    return (
        await asyncio_detailed(
            client=client,
            game_mode_id=game_mode_id,
            timecode=timecode,
            limit=limit,
            sort_by=sort_by,
            is_non_statcast=is_non_statcast,
            offset=offset,
            fields=fields,
        )
    ).parsed
