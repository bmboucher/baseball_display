from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.game_rest_object import GameRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    game_pk: str,
    *,
    timecode: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["timecode"] = timecode

    params["hydrate"] = hydrate

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1.1/game/{game_pk}/feed/live".format(
            game_pk=quote(str(game_pk), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GameRestObject | None:
    if response.status_code == 200:
        response_200 = GameRestObject.from_dict(response.json())

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
) -> Response[Any | GameRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    game_pk: str,
    *,
    client: AuthenticatedClient | Client,
    timecode: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | GameRestObject]:
    """View live game status. AKA GUMBO.

     **Description:**
    This endpoint returns the Gumbo Live Feed for a specific gamePk.

    **Return Includes:** Team information, live play by play data, and player information.

    **Required Parameters:** gamePk is required to run this call.

    **Hydrations:** This endpoint can accept the hydrations query parameter.

    <br></br>

    ---
    **Example of call with required parameters:**

    https://statsapi.mlb.com/api/v1.1/game/534196/feed/live

    ---
    **Example of call with all parameters:**

    https://statsapi.mlb.com/api/v1.1/game/534196/feed/live?timecode=20180323_014415&hydrate=alignment

    Args:
        game_pk (str):
        timecode (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GameRestObject]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        timecode=timecode,
        hydrate=hydrate,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    game_pk: str,
    *,
    client: AuthenticatedClient | Client,
    timecode: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | GameRestObject | None:
    """View live game status. AKA GUMBO.

     **Description:**
    This endpoint returns the Gumbo Live Feed for a specific gamePk.

    **Return Includes:** Team information, live play by play data, and player information.

    **Required Parameters:** gamePk is required to run this call.

    **Hydrations:** This endpoint can accept the hydrations query parameter.

    <br></br>

    ---
    **Example of call with required parameters:**

    https://statsapi.mlb.com/api/v1.1/game/534196/feed/live

    ---
    **Example of call with all parameters:**

    https://statsapi.mlb.com/api/v1.1/game/534196/feed/live?timecode=20180323_014415&hydrate=alignment

    Args:
        game_pk (str):
        timecode (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GameRestObject
    """

    return sync_detailed(
        game_pk=game_pk,
        client=client,
        timecode=timecode,
        hydrate=hydrate,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    game_pk: str,
    *,
    client: AuthenticatedClient | Client,
    timecode: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | GameRestObject]:
    """View live game status. AKA GUMBO.

     **Description:**
    This endpoint returns the Gumbo Live Feed for a specific gamePk.

    **Return Includes:** Team information, live play by play data, and player information.

    **Required Parameters:** gamePk is required to run this call.

    **Hydrations:** This endpoint can accept the hydrations query parameter.

    <br></br>

    ---
    **Example of call with required parameters:**

    https://statsapi.mlb.com/api/v1.1/game/534196/feed/live

    ---
    **Example of call with all parameters:**

    https://statsapi.mlb.com/api/v1.1/game/534196/feed/live?timecode=20180323_014415&hydrate=alignment

    Args:
        game_pk (str):
        timecode (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GameRestObject]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        timecode=timecode,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    game_pk: str,
    *,
    client: AuthenticatedClient | Client,
    timecode: str | Unset = UNSET,
    hydrate: Any | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | GameRestObject | None:
    """View live game status. AKA GUMBO.

     **Description:**
    This endpoint returns the Gumbo Live Feed for a specific gamePk.

    **Return Includes:** Team information, live play by play data, and player information.

    **Required Parameters:** gamePk is required to run this call.

    **Hydrations:** This endpoint can accept the hydrations query parameter.

    <br></br>

    ---
    **Example of call with required parameters:**

    https://statsapi.mlb.com/api/v1.1/game/534196/feed/live

    ---
    **Example of call with all parameters:**

    https://statsapi.mlb.com/api/v1.1/game/534196/feed/live?timecode=20180323_014415&hydrate=alignment

    Args:
        game_pk (str):
        timecode (str | Unset):
        hydrate (Any | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GameRestObject
    """

    return (
        await asyncio_detailed(
            game_pk=game_pk,
            client=client,
            timecode=timecode,
            hydrate=hydrate,
            fields=fields,
        )
    ).parsed
