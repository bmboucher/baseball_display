from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.high_low_org_type import HighLowOrgType
from ...models.high_low_wrapper_rest_object import HighLowWrapperRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_type: HighLowOrgType,
    *,
    stat_group: str | Unset = UNSET,
    sort_stat: str,
    season: str,
    game_type: str | Unset = UNSET,
    team_id: int | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_ids: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["statGroup"] = stat_group

    params["sortStat"] = sort_stat

    params["season"] = season

    params["gameType"] = game_type

    params["teamId"] = team_id

    params["leagueId"] = league_id

    params["sportIds"] = sport_ids

    params["limit"] = limit

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/highLow/{org_type}".format(
            org_type=quote(str(org_type), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HighLowWrapperRestObject | None:
    if response.status_code == 200:
        response_200 = HighLowWrapperRestObject.from_dict(response.json())

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
) -> Response[Any | HighLowWrapperRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_type: HighLowOrgType,
    *,
    client: AuthenticatedClient | Client,
    stat_group: str | Unset = UNSET,
    sort_stat: str,
    season: str,
    game_type: str | Unset = UNSET,
    team_id: int | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_ids: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | HighLowWrapperRestObject]:
    """View high/low stats by player or team.

     highLow

    Args:
        org_type (HighLowOrgType):
        stat_group (str | Unset):
        sort_stat (str):
        season (str):
        game_type (str | Unset):
        team_id (int | Unset):
        league_id (int | Unset):
        sport_ids (int | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HighLowWrapperRestObject]
    """

    kwargs = _get_kwargs(
        org_type=org_type,
        stat_group=stat_group,
        sort_stat=sort_stat,
        season=season,
        game_type=game_type,
        team_id=team_id,
        league_id=league_id,
        sport_ids=sport_ids,
        limit=limit,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_type: HighLowOrgType,
    *,
    client: AuthenticatedClient | Client,
    stat_group: str | Unset = UNSET,
    sort_stat: str,
    season: str,
    game_type: str | Unset = UNSET,
    team_id: int | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_ids: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | HighLowWrapperRestObject | None:
    """View high/low stats by player or team.

     highLow

    Args:
        org_type (HighLowOrgType):
        stat_group (str | Unset):
        sort_stat (str):
        season (str):
        game_type (str | Unset):
        team_id (int | Unset):
        league_id (int | Unset):
        sport_ids (int | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HighLowWrapperRestObject
    """

    return sync_detailed(
        org_type=org_type,
        client=client,
        stat_group=stat_group,
        sort_stat=sort_stat,
        season=season,
        game_type=game_type,
        team_id=team_id,
        league_id=league_id,
        sport_ids=sport_ids,
        limit=limit,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    org_type: HighLowOrgType,
    *,
    client: AuthenticatedClient | Client,
    stat_group: str | Unset = UNSET,
    sort_stat: str,
    season: str,
    game_type: str | Unset = UNSET,
    team_id: int | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_ids: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | HighLowWrapperRestObject]:
    """View high/low stats by player or team.

     highLow

    Args:
        org_type (HighLowOrgType):
        stat_group (str | Unset):
        sort_stat (str):
        season (str):
        game_type (str | Unset):
        team_id (int | Unset):
        league_id (int | Unset):
        sport_ids (int | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HighLowWrapperRestObject]
    """

    kwargs = _get_kwargs(
        org_type=org_type,
        stat_group=stat_group,
        sort_stat=sort_stat,
        season=season,
        game_type=game_type,
        team_id=team_id,
        league_id=league_id,
        sport_ids=sport_ids,
        limit=limit,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_type: HighLowOrgType,
    *,
    client: AuthenticatedClient | Client,
    stat_group: str | Unset = UNSET,
    sort_stat: str,
    season: str,
    game_type: str | Unset = UNSET,
    team_id: int | Unset = UNSET,
    league_id: int | Unset = UNSET,
    sport_ids: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | HighLowWrapperRestObject | None:
    """View high/low stats by player or team.

     highLow

    Args:
        org_type (HighLowOrgType):
        stat_group (str | Unset):
        sort_stat (str):
        season (str):
        game_type (str | Unset):
        team_id (int | Unset):
        league_id (int | Unset):
        sport_ids (int | Unset):
        limit (int | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HighLowWrapperRestObject
    """

    return (
        await asyncio_detailed(
            org_type=org_type,
            client=client,
            stat_group=stat_group,
            sort_stat=sort_stat,
            season=season,
            game_type=game_type,
            team_id=team_id,
            league_id=league_id,
            sport_ids=sport_ids,
            limit=limit,
            fields=fields,
        )
    ).parsed
