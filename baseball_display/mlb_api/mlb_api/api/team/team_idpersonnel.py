from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.roster_rest_object import RosterRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
    team_id: int,
    *,
    date: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["date"] = date

    json_fields: list[str] | Unset = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/teams/{team_id}/personnel".format(
            team_id=quote(str(team_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | RosterRestObject | None:
    if response.status_code == 200:
        response_200 = RosterRestObject.from_dict(response.json())

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
) -> Response[Any | RosterRestObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient | Client,
    date: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | RosterRestObject]:
    """View biographical  information on all personnel for a given club.

     **Description:**
     This endpoint allows you return a directory of personnel for a particular team.

     **Return Includes:** fullName, job,jobID and profile link.

     **Required Parameters:** teamId is required to run this call.

     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/109/personnel


    Args:
        team_id (int):
        date (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | RosterRestObject]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        date=date,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    team_id: int,
    *,
    client: AuthenticatedClient | Client,
    date: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | RosterRestObject | None:
    """View biographical  information on all personnel for a given club.

     **Description:**
     This endpoint allows you return a directory of personnel for a particular team.

     **Return Includes:** fullName, job,jobID and profile link.

     **Required Parameters:** teamId is required to run this call.

     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/109/personnel


    Args:
        team_id (int):
        date (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | RosterRestObject
    """

    return sync_detailed(
        team_id=team_id,
        client=client,
        date=date,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    team_id: int,
    *,
    client: AuthenticatedClient | Client,
    date: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | RosterRestObject]:
    """View biographical  information on all personnel for a given club.

     **Description:**
     This endpoint allows you return a directory of personnel for a particular team.

     **Return Includes:** fullName, job,jobID and profile link.

     **Required Parameters:** teamId is required to run this call.

     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/109/personnel


    Args:
        team_id (int):
        date (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | RosterRestObject]
    """

    kwargs = _get_kwargs(
        team_id=team_id,
        date=date,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    team_id: int,
    *,
    client: AuthenticatedClient | Client,
    date: str | Unset = UNSET,
    fields: list[str] | Unset = UNSET,
) -> Any | RosterRestObject | None:
    """View biographical  information on all personnel for a given club.

     **Description:**
     This endpoint allows you return a directory of personnel for a particular team.

     **Return Includes:** fullName, job,jobID and profile link.

     **Required Parameters:** teamId is required to run this call.

     ---
     **Example of call with required parameters**

     https://statsapi.mlb.com/api/v1/teams/109/personnel


    Args:
        team_id (int):
        date (str | Unset):
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | RosterRestObject
    """

    return (
        await asyncio_detailed(
            team_id=team_id,
            client=client,
            date=date,
            fields=fields,
        )
    ).parsed
