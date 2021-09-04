[**Эта страница доступна на русском языке**](/docs/README.md)

# Mastodon meter

Mastodon meter is an open analytics system for the [Mastodon federated social network](https://joinmastodon.org).

### Capabilities of Mastodon meter:

- Add and remove accounts from the watch list;
- Schedule (daily by default) tasks to gather measurements for each of the accounts in the watch list:
  Obtain a counter of subscribers and statuses and save them to the database;
- Generate graphs and text reports based on the data gathered;
- Provides a convenient API interface to use in your own projects, including getting the raw data for further
  processing;

### Advantages of Mastodon meter:

- **Fast and lightweight**. Mastodon meter uses the modern asynchronous web framework FastAPI, asynchronous Motor and
  HttpX libraries. This makes it fast while consuming minimal resources (several times quicker response time compared to
  synchronous alternatives);
- **Robust**. Thanks to the technologies used, the server can handle hundreds or thousands of monitored accounts without
  any significant performance loss. Scalability is built into the solution's architecture;
- **Modern technologies**. The solution is based on modern libraries such as FastAPI and HttpX, a non-relational MongoDB
  database, Asynchronous style. Poetry is used for dependency management and Loguru is responsible for logging;
- **Easy maintenance**. The entire codebase is PEP8 compliant, and type annotated. This fact makes it easier to maintain
  and contribute to. Type annotations also enable usage of static analysis, which reduces the number of bugs and
  increases code quality;
- **Reliability**. Validation of incoming and outgoing requests using Pydantic makes it hard to "put the API down"
  with invalid requests.

### Technologies used:

- Asynchronous web framework **FastAPI**;
- **Pydantic** validation library;
- Asynchronous library for handling HTTP requests **HttpX**;
- **Loguru** logging module;
- **MongoDB** non-relational database ;
- Asynchronous client for MongoDB **Motor**;
- Graph generation - **Matplotlib**;
- **Uvicorn** ASGI server;
- Static analysis, formatting, linting: **Mypy, Black, Flake8**.

### Installation and startup

1. Install Poetry following the official [manual](https://python-poetry.org/docs/):
   `$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

2. Clone the repository and navigate inside: `$ git clone https://github.com/arseniiarsenii/mastodon-meter.git
   && cd mastodon-meter`.

3. Install dependencies in a virtual environment using Poetry and load it: `$ poetry install --no-dev && poetry shell`

Export [connection address](https://docs.mongodb.com/guides/server/drivers/) for the MongoDB database to the environment
variables: `$ export MONGO_CONNECTION_URL="mongodb+srv://your_connection_string_here"`

5. Go to the source directory and start the server: `$ cd src && uvicorn app:app`

The server is up and running at `http://127.0.0.1:8000`.

### Development.

You can take part in the development of Mastodon-meter. To do so, make a fork of this repository, make changes to it,
and send a pull request.

This solution is distributed under the [GNU GPL v3] license (https://www.gnu.org/licenses/gpl-3.0.en.html). Commercial
usage and source closing is not allowed.


---

# API documentation

## Operations with the list of tracked accounts

### Add an account to your watch list

**POST** request to `/api/accounts/add`

#### REQUEST PAYLOAD

```json
{
  "instance": "https://mastodon.social",
  "instance_id": "000000",
  "username": "example"
}
```

#### RESPONSE PAYLOAD

Success:

```json
{
  "status": true,
  "message": "Description for the operation result",
  "account_internal_id": "1447ab4fd6924e4cb11038bb487a761d"
}
```

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Remove an account from the tracked list

**POST** request to `/api/accounts/remove`

#### REQUEST PAYLOAD

```json
{
  "account_internal_id": "1447ab4fd6924e4cb11038bb487a761d",
  "remove_associated_data": false
}
```

#### RESPONSE PAYLOAD

Success:

```json
{
  "status": true,
  "message": "Description for the operation result"
}
```

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Get a list of tracked accounts

**GET** request to `/api/accounts/tracked`

#### RESPONSE PAYLOAD

Success:

```json
{
  "status": true,
  "message": "Description for the operation result",
  "tracked_accounts": [
    {
      "internal_id": "1447ab4fd6924e4cb11038bb487a761d",
      "username": "example",
      "instance": "https://mastodon.social",
      "instance_id": "000000",
      "added_on": "2021-01-01 12:00:00.000000"
    },
    {
      "internal_id": "1447ab4fd6924e4cb11038bb487a761d",
      "username": "example",
      "instance": "https://mastodon.social",
      "instance_id": "000000",
      "added_on": "2021-01-01 12:00:00.000000"
    }
  ]
}
```

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Collect data for all the tracked accounts and save it in the database

**GET** request to `/api/gather-data`

#### RESPONSE PAYLOAD

Success:

```json
{
  "status": true,
  "message": "Description for the operation result"
}
```

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

## Operations on accounts from the tracked list

### Get raw data for a specific period

**GET** request to `/api/{account_internal_id}/data`

#### REQUEST PAYLOAD

```json
{
  "since": "2021-01-01 12:00",
  "to": null
}
```

The `since` and `to` parameters determine the time period for which the data will be retrieved. These parameters take
either the value
`null` - no restriction, or a string of the form `2021-01-01 12:00`. Correspondingly, if both parameters are equal to
`null` - all available data will be retrieved.

#### RESPONSE PAYLOAD

Success:

```json
{
  "status": true,
  "message": "Description for the operation result",
  "data": [
    {
      "toot_count": 100,
      "subscribers_count": 250,
      "metering_id": "1447ab4fd6924e4cb11038bb487a761d",
      "timestamp": "2021-01-01 12:00:00.000000"
    },
    {
      "toot_count": 100,
      "subscribers_count": 250,
      "metering_id": "1447ab4fd6924e4cb11038bb487a761d",
      "timestamp": "2021-01-01 12:00:00.000000"
    }
  ]
}
```

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Get a graph of subscriber history for a specific period

**GET** request to `/api/{account_internal_id}/graph/subscribers`

#### REQUEST PAYLOAD

```json
{
  "since": "2021-01-01 12:00",
  "to": null
}
```

The `since` and `to` parameters determine the time period for which the data will be retrieved. These parameters take
either the value
`null` - no restriction, or a string of the form `2021-01-01 12:00`. Correspondingly, if both parameters are equal to
`null` - all available data will be retrieved.

#### RESPONSE PAYLOAD

Success:
File with the `.png` extension

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Get a graph of the publication history for a certain period

**GET** request to `/api/{account_internal_id}/graph/toots`

#### REQUEST PAYLOAD

```json
{
  "since": "2021-01-01 12:00",
  "to": null
}
```

The `since` and `to` parameters determine the time period for which the data will be retrieved. These parameters take
either the value
`null` - no restriction, or a string of the form `2021-01-01 12:00`. Correspondingly, if both parameters are equal to
`null` - all available data will be retrieved.

#### RESPONSE PAYLOAD

Success:
File with the `.png` extension

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Get a common graph of the history of publications and subscribers for a certain period

**GET** request to `/api/{account_internal_id}/graph/common`

#### REQUEST PAYLOAD

```json
{
  "since": "2021-01-01 12:00",
  "to": null
}
```

The `since` and `to` parameters determine the time period for which the data will be retrieved. These parameters take
either the value
`null` - no restriction, or a string of the form `2021-01-01 12:00`. Correspondingly, if both parameters are equal to
`null` - all available data will be retrieved.

#### RESPONSE PAYLOAD

Success:
File with the `.png` extension

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Get a simple text report on the accounts you're tracking

Returns a text response similar to:

```
Mastodon-meter summary report generated on 2021.09.01 09:00 UTC

account_name_1@mastodon.social: 102 subscribers, 2000 (+2) statuses
account_name_2@mastodon.social: 94 subscribers, 735 statuses
account_name_3@mastodon.social: 39 subscribers, 4671 (+5) statuses
...
account_name_n@mastodon.social: 45 subscribers, 118 statuses
```

Useful for sending over email or using in a chat-bot.

**GET** request to `/api/{account_internal_id}/graph/common`

#### REQUEST PAYLOAD

In the `accounts` field you must specify a list of internal account IDs that will be included in the report

```json
{
  "accounts": [
    "001a24eb90864bf2ba046f36f74f3a8a",
    "0ffc53bbeca947f69536f141f2df20cf",
    "da20f348160b418aa5d158baade0d366"
  ]
}
```

If the field is set to `null` - the report will be generated for all the tracked accounts

```json
{
  "accounts": null
}
```

#### RESPONSE PAYLOAD

Success:

```json
{
  "status": true,
  "message": "Description for the operation result",
  "report": "Simple text report"
}
```

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```
