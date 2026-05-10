from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.play_by_play_rest_object import PlayByPlayRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    game_pk: str,
    guid: str,
    *,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["hydrate"] = hydrate

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/game/{game_pk}/{guid}/analytics".format(
            game_pk=quote(str(game_pk), safe=""),
            guid=quote(str(guid), safe=""),
        ),
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
    game_pk: str,
    guid: str,
    *,
    client: AuthenticatedClient | Client,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | PlayByPlayRestObject]:
    """View Statcast data for a specific play.

     **Description:**
    This endpoint returns Statcast data for a specific play.

    **Return Includes:** timestamps.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/game/566532/17c0551a-4caa-476b-9208-5d3cb5f58b7d/analytics?

    ---

    **Example of call with hydration parameters**

    https://statsapi.mlb.com/api/v1/game/566532/17c0551a-4caa-476b-9208-
    5d3cb5f58b7d/analytics?hydrate=analytics(hit,pitch,ball,metrics,video,positions,diagram)

    Args:
        game_pk (str):
        guid (str):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PlayByPlayRestObject]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        guid=guid,
        hydrate=hydrate,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    game_pk: str,
    guid: str,
    *,
    client: AuthenticatedClient | Client,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | PlayByPlayRestObject | None:
    """View Statcast data for a specific play.

     **Description:**
    This endpoint returns Statcast data for a specific play.

    **Return Includes:** timestamps.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/game/566532/17c0551a-4caa-476b-9208-5d3cb5f58b7d/analytics?

    ---

    **Example of call with hydration parameters**

    https://statsapi.mlb.com/api/v1/game/566532/17c0551a-4caa-476b-9208-
    5d3cb5f58b7d/analytics?hydrate=analytics(hit,pitch,ball,metrics,video,positions,diagram)

    Args:
        game_pk (str):
        guid (str):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PlayByPlayRestObject
    """

    return sync_detailed(
        game_pk=game_pk,
        guid=guid,
        client=client,
        hydrate=hydrate,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    game_pk: str,
    guid: str,
    *,
    client: AuthenticatedClient | Client,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | PlayByPlayRestObject]:
    """View Statcast data for a specific play.

     **Description:**
    This endpoint returns Statcast data for a specific play.

    **Return Includes:** timestamps.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/game/566532/17c0551a-4caa-476b-9208-5d3cb5f58b7d/analytics?

    ---

    **Example of call with hydration parameters**

    https://statsapi.mlb.com/api/v1/game/566532/17c0551a-4caa-476b-9208-
    5d3cb5f58b7d/analytics?hydrate=analytics(hit,pitch,ball,metrics,video,positions,diagram)

    Args:
        game_pk (str):
        guid (str):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PlayByPlayRestObject]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        guid=guid,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    game_pk: str,
    guid: str,
    *,
    client: AuthenticatedClient | Client,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | PlayByPlayRestObject | None:
    """View Statcast data for a specific play.

     **Description:**
    This endpoint returns Statcast data for a specific play.

    **Return Includes:** timestamps.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/game/566532/17c0551a-4caa-476b-9208-5d3cb5f58b7d/analytics?

    ---

    **Example of call with hydration parameters**

    https://statsapi.mlb.com/api/v1/game/566532/17c0551a-4caa-476b-9208-
    5d3cb5f58b7d/analytics?hydrate=analytics(hit,pitch,ball,metrics,video,positions,diagram)

    Args:
        game_pk (str):
        guid (str):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PlayByPlayRestObject
    """

    return (
        await asyncio_detailed(
            game_pk=game_pk,
            guid=guid,
            client=client,
            hydrate=hydrate,
            fields=fields,
        )
    ).parsed
