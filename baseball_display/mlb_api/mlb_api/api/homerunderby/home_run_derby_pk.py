from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.home_run_derby_rest_object import HomeRunDerbyRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    game_pk: int,
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
        "url": "/v1/homeRunDerby/{game_pk}".format(
            game_pk=quote(str(game_pk), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HomeRunDerbyRestObject | None:
    if response.status_code == 200:
        response_200 = HomeRunDerbyRestObject.from_dict(response.json())

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
) -> Response[Any | HomeRunDerbyRestObject]:
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
    fields: list[str] | Unset = UNSET,
) -> Response[Any | HomeRunDerbyRestObject]:
    """View a home run derby object based on gamePk.


    **Description:**
    This endpoint returns HomerunDerby data for a specific gamePk.

    **Return Includes:** Round breakdown, hit data, player information.

    **Required Parameters:** gamePk is required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/homeRunDerby/511101

    Args:
        game_pk (int):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HomeRunDerbyRestObject]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    game_pk: int,
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Any | HomeRunDerbyRestObject | None:
    """View a home run derby object based on gamePk.


    **Description:**
    This endpoint returns HomerunDerby data for a specific gamePk.

    **Return Includes:** Round breakdown, hit data, player information.

    **Required Parameters:** gamePk is required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/homeRunDerby/511101

    Args:
        game_pk (int):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HomeRunDerbyRestObject
    """

    return sync_detailed(
        game_pk=game_pk,
        client=client,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    game_pk: int,
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | HomeRunDerbyRestObject]:
    """View a home run derby object based on gamePk.


    **Description:**
    This endpoint returns HomerunDerby data for a specific gamePk.

    **Return Includes:** Round breakdown, hit data, player information.

    **Required Parameters:** gamePk is required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/homeRunDerby/511101

    Args:
        game_pk (int):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HomeRunDerbyRestObject]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    game_pk: int,
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Any | HomeRunDerbyRestObject | None:
    """View a home run derby object based on gamePk.


    **Description:**
    This endpoint returns HomerunDerby data for a specific gamePk.

    **Return Includes:** Round breakdown, hit data, player information.

    **Required Parameters:** gamePk is required to run this call.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/homeRunDerby/511101

    Args:
        game_pk (int):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HomeRunDerbyRestObject
    """

    return (
        await asyncio_detailed(
            game_pk=game_pk,
            client=client,
            fields=fields,
        )
    ).parsed
