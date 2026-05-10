from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.situation_code_rest_object import SituationCodeRestObject
from ...types import UNSET, Response, Unset


def _get_kwargs(
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
        "url": "/v1/situationCodes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list[SituationCodeRestObject] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SituationCodeRestObject.from_dict(
                response_200_item_data
            )

            response_200.append(response_200_item)

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
) -> Response[Any | list[SituationCodeRestObject]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | list[SituationCodeRestObject]]:
    """Situation codes


    **Description:**
    This endpoint returns all situational codes available on the Stats API.

    **Return Includes:** situationCodes.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/situationCodes

    Args:
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[SituationCodeRestObject]]
    """

    kwargs = _get_kwargs(
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Any | list[SituationCodeRestObject] | None:
    """Situation codes


    **Description:**
    This endpoint returns all situational codes available on the Stats API.

    **Return Includes:** situationCodes.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/situationCodes

    Args:
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[SituationCodeRestObject]
    """

    return sync_detailed(
        client=client,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Response[Any | list[SituationCodeRestObject]]:
    """Situation codes


    **Description:**
    This endpoint returns all situational codes available on the Stats API.

    **Return Includes:** situationCodes.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/situationCodes

    Args:
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[SituationCodeRestObject]]
    """

    kwargs = _get_kwargs(
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    fields: list[str] | Unset = UNSET,
) -> Any | list[SituationCodeRestObject] | None:
    """Situation codes


    **Description:**
    This endpoint returns all situational codes available on the Stats API.

    **Return Includes:** situationCodes.

    **Required Parameters:** No parameters are required to run this call.

    ---
    **Example of call with all parameters**

    https://statsapi.mlb.com/api/v1/situationCodes

    Args:
        fields (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[SituationCodeRestObject]
    """

    return (
        await asyncio_detailed(
            client=client,
            fields=fields,
        )
    ).parsed
