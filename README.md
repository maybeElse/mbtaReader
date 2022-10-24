# mbtaReader

A python wrapper for the [MBTA API v3](https://www.mbta.com/developers/v3-api)

## Introduction

While several python wrappers for the MBTA's API already exist, none of the implement the *entire* API. This situation is now less dire than it was when I first started (ie, pymbta3 added support for the `predictions` endpoint in August), but it still matters to me for some reason.

Depending on your needs, it may be preferable to use a more mature API wrapper such as [pymbta3](https://github.com/altonplace/pymbta3).

## Usage

First, request an API key on the [MBTA's developer portal](https://api-v3.mbta.com/). Or don't! Running with an API key limits you to 20 requests/minute.

    import mbtaReader
    api = MBTAReader(
        key = `your API key`
    )

Then you can use the various methods.

    api.get_line_by_id(id='line-Red',include=('routes'))
    # get information about the Red Line and the routes it's associated with

    api.get_stops(route='Shuttle-AlewifeHarvard')
    # get information about stops serviced by one of the Red Line's bus bridges

    api.get_prediction(stop='place-harsq', limit='3', direction_id='0', route_type='1')
    # get the next 3 southbound trains at Harvard Square station

MBTAReader offers a `get_` method corresponding to each endpoint documented in the MBTA's API. Their documentation is thorough and not at all scary, so I suggest going over there to learn about the various arguments which can be passed into the API!

## TODO

- Error handling (identify when the API returns an error, and throw an exception instead of silently passing it onwards)
- Objects for each return type, to make things easier to interact with
- Test cases for each method
- Little a documentation, as a treat?