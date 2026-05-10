from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    game_pk: int,
    *,
    start_timecode: str,
    end_timecode: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["startTimecode"] = start_timecode

    params["endTimecode"] = end_timecode

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1.1/game/{game_pk}/feed/live/diffPatch".format(
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
    start_timecode: str,
    end_timecode: str,
) -> Response[Any]:
    """View differences between two timecodes in live game.

     **Description:**
    This endpoint returns the difference/discrepancies between two timecodes in the Gumbo Live Feed
    using the Diff Patch System.

    **Return Includes:** Play by play data and player information.
    <br/><br/><b>Diff/Patch
    System:</b> startTimecode and endTimecode can be used for getting
    diffs.<br/>Expected usage:  <br/> 1) Request full payload by not passing
    startTimecode or endTimecode.  This will return the most recent game
    state.<br/> 2) Find the latest timecode in this response.  <br/> 3) Wait
    X seconds<br/> 4) Use the timecode from step 2 above as the startTimecode.  This
    will give you a diff of everything that has happened since
    startTimecode.  <br/> 5) If no data is returned, wait X seconds and do
    the same request.  <br/> 6) If data is returned, get a new timeStamp
    from the response, and use that for the next call as startTimecode.
    <br></br>
    **Required Parameters:** all parameters are required to run this call. If incorrectly called the
    call will default to http://statsapi.mlb.com/api/v1.1/game/531304/feed/live
    <br></br>

    ---
    **Example of call with required parameters:**

    http://statsapi.mlb.com/api/v1.1/game/531321/feed/live/diffPatch?startTimecode=20180823_193704&endTi
    mecode=20180823_193711

    Args:
        game_pk (int):
        start_timecode (str):
        end_timecode (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        start_timecode=start_timecode,
        end_timecode=end_timecode,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    game_pk: int,
    *,
    client: AuthenticatedClient | Client,
    start_timecode: str,
    end_timecode: str,
) -> Response[Any]:
    """View differences between two timecodes in live game.

     **Description:**
    This endpoint returns the difference/discrepancies between two timecodes in the Gumbo Live Feed
    using the Diff Patch System.

    **Return Includes:** Play by play data and player information.
    <br/><br/><b>Diff/Patch
    System:</b> startTimecode and endTimecode can be used for getting
    diffs.<br/>Expected usage:  <br/> 1) Request full payload by not passing
    startTimecode or endTimecode.  This will return the most recent game
    state.<br/> 2) Find the latest timecode in this response.  <br/> 3) Wait
    X seconds<br/> 4) Use the timecode from step 2 above as the startTimecode.  This
    will give you a diff of everything that has happened since
    startTimecode.  <br/> 5) If no data is returned, wait X seconds and do
    the same request.  <br/> 6) If data is returned, get a new timeStamp
    from the response, and use that for the next call as startTimecode.
    <br></br>
    **Required Parameters:** all parameters are required to run this call. If incorrectly called the
    call will default to http://statsapi.mlb.com/api/v1.1/game/531304/feed/live
    <br></br>

    ---
    **Example of call with required parameters:**

    http://statsapi.mlb.com/api/v1.1/game/531321/feed/live/diffPatch?startTimecode=20180823_193704&endTi
    mecode=20180823_193711

    Args:
        game_pk (int):
        start_timecode (str):
        end_timecode (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        game_pk=game_pk,
        start_timecode=start_timecode,
        end_timecode=end_timecode,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
