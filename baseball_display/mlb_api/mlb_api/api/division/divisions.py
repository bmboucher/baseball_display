from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.divisions_rest_object import DivisionsRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_id: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["divisionId"] = division_id

    params["leagueId"] = league_id

    params["sportId"] = sport_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/divisions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | DivisionsRestObject | None:
    if response.status_code == 200:
        response_200 = DivisionsRestObject.from_dict(response.json())

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
) -> Response[Any | DivisionsRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_id: int | Unset = UNSET,
) -> Response[Any | DivisionsRestObject]:
    """View a directory of divisions.


    **Description:**
    This endpoint returns a directory of division(s) based on divisionId,leagueId,&sportId.

    **Return Includes:** Division name, id, leagueId, & sportId.

    **Required Parameters:** No parameters are required to run this call.
    <br></br>

    **To return all divisionIds among all sports and leagues run call with no parameters.**

    ---
    **Example of call with no parameters:**

    https://statsapi.mlb.com/api/v1/divisions

    ---
    **Example of call with all parameters:**

    https://statsapi.mlb.com/api/v1/divisions?divisionId=200&leagueId=103&sportId=1

    Args:
        division_id (str | Unset):
        league_id (int | Unset):
        sport_id (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DivisionsRestObject]
    """

    kwargs = _get_kwargs(
        division_id=division_id,
        league_id=league_id,
        sport_id=sport_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_id: int | Unset = UNSET,
) -> Any | DivisionsRestObject | None:
    """View a directory of divisions.


    **Description:**
    This endpoint returns a directory of division(s) based on divisionId,leagueId,&sportId.

    **Return Includes:** Division name, id, leagueId, & sportId.

    **Required Parameters:** No parameters are required to run this call.
    <br></br>

    **To return all divisionIds among all sports and leagues run call with no parameters.**

    ---
    **Example of call with no parameters:**

    https://statsapi.mlb.com/api/v1/divisions

    ---
    **Example of call with all parameters:**

    https://statsapi.mlb.com/api/v1/divisions?divisionId=200&leagueId=103&sportId=1

    Args:
        division_id (str | Unset):
        league_id (int | Unset):
        sport_id (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DivisionsRestObject
    """

    return sync_detailed(
        client=client,
        division_id=division_id,
        league_id=league_id,
        sport_id=sport_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_id: int | Unset = UNSET,
) -> Response[Any | DivisionsRestObject]:
    """View a directory of divisions.


    **Description:**
    This endpoint returns a directory of division(s) based on divisionId,leagueId,&sportId.

    **Return Includes:** Division name, id, leagueId, & sportId.

    **Required Parameters:** No parameters are required to run this call.
    <br></br>

    **To return all divisionIds among all sports and leagues run call with no parameters.**

    ---
    **Example of call with no parameters:**

    https://statsapi.mlb.com/api/v1/divisions

    ---
    **Example of call with all parameters:**

    https://statsapi.mlb.com/api/v1/divisions?divisionId=200&leagueId=103&sportId=1

    Args:
        division_id (str | Unset):
        league_id (int | Unset):
        sport_id (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DivisionsRestObject]
    """

    kwargs = _get_kwargs(
        division_id=division_id,
        league_id=league_id,
        sport_id=sport_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    division_id: str | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_id: int | Unset = UNSET,
) -> Any | DivisionsRestObject | None:
    """View a directory of divisions.


    **Description:**
    This endpoint returns a directory of division(s) based on divisionId,leagueId,&sportId.

    **Return Includes:** Division name, id, leagueId, & sportId.

    **Required Parameters:** No parameters are required to run this call.
    <br></br>

    **To return all divisionIds among all sports and leagues run call with no parameters.**

    ---
    **Example of call with no parameters:**

    https://statsapi.mlb.com/api/v1/divisions

    ---
    **Example of call with all parameters:**

    https://statsapi.mlb.com/api/v1/divisions?divisionId=200&leagueId=103&sportId=1

    Args:
        division_id (str | Unset):
        league_id (int | Unset):
        sport_id (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DivisionsRestObject
    """

    return (
        await asyncio_detailed(
            client=client,
            division_id=division_id,
            league_id=league_id,
            sport_id=sport_id,
        )
    ).parsed
