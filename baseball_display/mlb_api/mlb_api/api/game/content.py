from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    game_pk: int,
    *,
    highlight_limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["highlightLimit"] = highlight_limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/game/{game_pk}/content".format(
            game_pk=quote(str(game_pk), safe=""),
        ),
        "params": params,
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
    game_pk: int,
    *,
    client: AuthenticatedClient | Client,
    highlight_limit: int | Unset = UNSET,
) -> Response[Any]:
    """View all content for a game.


    **Description:**
    This endpoint returns editorial content for a specific gamePk.

    **Return Includes:** Editorial pieces, highlights, images, game summary and game notes.

    **Required Parameters:** gamePk is required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/game/531060/content

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/game/531060/content?highlightLimit=5

    Args:
        game_pk (int):
        highlight_limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        highlight_limit=highlight_limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    game_pk: int,
    *,
    client: AuthenticatedClient | Client,
    highlight_limit: int | Unset = UNSET,
) -> Response[Any]:
    """View all content for a game.


    **Description:**
    This endpoint returns editorial content for a specific gamePk.

    **Return Includes:** Editorial pieces, highlights, images, game summary and game notes.

    **Required Parameters:** gamePk is required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/game/531060/content

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/game/531060/content?highlightLimit=5

    Args:
        game_pk (int):
        highlight_limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        highlight_limit=highlight_limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
