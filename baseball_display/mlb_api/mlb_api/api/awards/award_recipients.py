from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    award_id: str,
    *,
    sport_id: int | Unset = UNSET,
    league_id: list[int] | Unset = UNSET,
    season: list[int] | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["sportId"] = sport_id

    json_league_id: list[int] | Unset = UNSET
    if not isinstance(league_id, Unset):
        json_league_id = league_id

    params["leagueId"] = json_league_id

    json_season: list[int] | Unset = UNSET
    if not isinstance(season, Unset):
        json_season = season

    params["season"] = json_season

    json_hydrate: list[str] | Unset = UNSET
    if not isinstance(hydrate, Unset):
        json_hydrate = hydrate

    params["hydrate"] = json_hydrate

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/awards/{award_id}/recipients".format(
            award_id=quote(str(award_id), safe=""),
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
    award_id: str,
    *,
    client: AuthenticatedClient | Client,
    sport_id: int | Unset = UNSET,
    league_id: list[int] | Unset = UNSET,
    season: list[int] | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View recipients of an award.

     **Description:**
    This endpoint returns awards data based on awardId.

    **Return Includes:** recipients, team, position, year.

    **Required Parameters:** awardId is required to run this call.

    **Hydrations:** This endpoint can accept the hydrations query parameter.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/awards/MLBHOF/recipients?
    <br> </br>

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/awards/MLBHOF/recipients?sportId=1&season=2017&leagueId=103

    Args:
        award_id (str):
        sport_id (int | Unset):
        league_id (list[int] | Unset):
        season (list[int] | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        award_id=award_id,
        sport_id=sport_id,
        league_id=league_id,
        season=season,
        hydrate=hydrate,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    award_id: str,
    *,
    client: AuthenticatedClient | Client,
    sport_id: int | Unset = UNSET,
    league_id: list[int] | Unset = UNSET,
    season: list[int] | Unset = UNSET,
    hydrate: list[str] | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any]:
    """View recipients of an award.

     **Description:**
    This endpoint returns awards data based on awardId.

    **Return Includes:** recipients, team, position, year.

    **Required Parameters:** awardId is required to run this call.

    **Hydrations:** This endpoint can accept the hydrations query parameter.

    ---
    **Example of call with required parameters**

    https://statsapi.mlb.com/api/v1/awards/MLBHOF/recipients?
    <br> </br>

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/awards/MLBHOF/recipients?sportId=1&season=2017&leagueId=103

    Args:
        award_id (str):
        sport_id (int | Unset):
        league_id (list[int] | Unset):
        season (list[int] | Unset):
        hydrate (list[str] | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        award_id=award_id,
        sport_id=sport_id,
        league_id=league_id,
        season=season,
        hydrate=hydrate,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
