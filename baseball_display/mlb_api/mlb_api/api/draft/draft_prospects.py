from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.draft_prospects_position import DraftProspectsPosition
from ...types import UNSET, Response, Unset


def _get_kwargs(
    year: int,
    *,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    round_: str | Unset = UNSET,
    name: str | Unset = UNSET,
    school: str | Unset = UNSET,
    state: str | Unset = UNSET,
    country: str | Unset = UNSET,
    position: DraftProspectsPosition | Unset = UNSET,
    team_id: int | Unset = UNSET,
    player_id: int | Unset = UNSET,
    bis_player_id: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params["round"] = round_

    params["name"] = name

    params["school"] = school

    params["state"] = state

    params["country"] = country

    json_position: str | Unset = UNSET
    if not isinstance(position, Unset):
        json_position = position.value

    params["position"] = json_position

    params["teamId"] = team_id

    params["playerId"] = player_id

    params["bisPlayerId"] = bis_player_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/draft/prospects/{year}".format(
            year=quote(str(year), safe=""),
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
    year: int,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    round_: str | Unset = UNSET,
    name: str | Unset = UNSET,
    school: str | Unset = UNSET,
    state: str | Unset = UNSET,
    country: str | Unset = UNSET,
    position: DraftProspectsPosition | Unset = UNSET,
    team_id: int | Unset = UNSET,
    player_id: int | Unset = UNSET,
    bis_player_id: int | Unset = UNSET,
) -> Response[Any]:
    """View draft eligible prospects by year.


    **Description:**
    This endpoint returns biographical and financial data for Rule 4 draft eligible prospects.

    **Return Includes:** Player name, id, financial data, & team data.

    **Required Parameters:** year is required to run this call.

    ---
    **Example of call with required parameters:**

     https://statsapi.mlb.com/api/v1/draft/prospects/2018

    ---
    **Example of call with all parameters:**

     https://statsapi.mlb.com/api/v1/draft/prospects/2018?limit=1&round=1&name=M&school=A&position=P&tea
    mId=116&playerId=663554&bisPlayerId=759143

    Args:
        year (int):
        limit (int | Unset):
        fields (list[str] | Unset):
        round_ (str | Unset):
        name (str | Unset):
        school (str | Unset):
        state (str | Unset):
        country (str | Unset):
        position (DraftProspectsPosition | Unset):
        team_id (int | Unset):
        player_id (int | Unset):
        bis_player_id (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        year=year,
        limit=limit,
        fields=fields,
        round_=round_,
        name=name,
        school=school,
        state=state,
        country=country,
        position=position,
        team_id=team_id,
        player_id=player_id,
        bis_player_id=bis_player_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    year: int,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
    round_: str | Unset = UNSET,
    name: str | Unset = UNSET,
    school: str | Unset = UNSET,
    state: str | Unset = UNSET,
    country: str | Unset = UNSET,
    position: DraftProspectsPosition | Unset = UNSET,
    team_id: int | Unset = UNSET,
    player_id: int | Unset = UNSET,
    bis_player_id: int | Unset = UNSET,
) -> Response[Any]:
    """View draft eligible prospects by year.


    **Description:**
    This endpoint returns biographical and financial data for Rule 4 draft eligible prospects.

    **Return Includes:** Player name, id, financial data, & team data.

    **Required Parameters:** year is required to run this call.

    ---
    **Example of call with required parameters:**

     https://statsapi.mlb.com/api/v1/draft/prospects/2018

    ---
    **Example of call with all parameters:**

     https://statsapi.mlb.com/api/v1/draft/prospects/2018?limit=1&round=1&name=M&school=A&position=P&tea
    mId=116&playerId=663554&bisPlayerId=759143

    Args:
        year (int):
        limit (int | Unset):
        fields (list[str] | Unset):
        round_ (str | Unset):
        name (str | Unset):
        school (str | Unset):
        state (str | Unset):
        country (str | Unset):
        position (DraftProspectsPosition | Unset):
        team_id (int | Unset):
        player_id (int | Unset):
        bis_player_id (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        year=year,
        limit=limit,
        fields=fields,
        round_=round_,
        name=name,
        school=school,
        state=state,
        country=country,
        position=position,
        team_id=team_id,
        player_id=player_id,
        bis_player_id=bis_player_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
