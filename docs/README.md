# Mastodon meter

---

# API

## Операции со списком отслеживаемых аккаунтов

### Добавить аккаунт в список отслеживаемых
**POST** запрос на `/api/accounts/add`

#### REQUEST PAYLOAD
```json
{
  "instance": "https://mastodon.social",
  "instance_id": "000000"
}
```

#### RESPONSE PAYLOAD
Success:
```json
{
  "status":  true,
  "account_internal_id": "1447ab4fd6924e4cb11038bb487a761d",
  "message": "Description for the operation result"
}
```

Error:
```json
{
  "status":  false,
  "message": "Description for the operation result"
}
```


### Удалить аккаунт из списка отслеживаемых
**POST** запрос на `/api/accounts/remove`

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
  "status":  true,
  "message": "Description for the operation result"
}
```

Error:
```json
{
  "status":  false,
  "message": "Description for the operation result"
}
```

### Получить список отслеживаемых аккаунтов
**GET** запрос на `/api/accounts/tracked`

#### RESPONSE PAYLOAD
Success:
```json
{
  "status":  true,
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
  "status":  false,
  "message": "Description for the operation result"
}
```

## Операции с аккаунтами из списка отслеживаемых

### Получить сырые данные за определенный период
**GET** запрос на `/api/{account_internal_id}/data`
#### REQUEST PAYLOAD
```json
{
  "from": "2021-01-01 12:00",
  "to": null
}
```

Параметры `from` и `to` определяют срок, за который будут получены данные. Эти параметры принимают либо значение 
`null` - ограничение отсутствует, либо строка вида `2021-01-01 12:00`. Соответственно, если оба параметра равны 
`null` - будут получены все доступные данные.

#### RESPONSE PAYLOAD
Success:
```json
{
  "status":  true,
  "message": "Description for the operation result",
  "account_internal_id": "1447ab4fd6924e4cb11038bb487a761d",
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
  "status":  false,
  "message": "Description for the operation result"
}
```

### Получить график истории подписчиков за определенный период
**GET** запрос на `/api/{account_internal_id}/subscribers/graph`
#### REQUEST PAYLOAD
```json
{
  "from": "2021-01-01 12:00",
  "to": null
}
```

Параметры `from` и `to` определяют срок, за который будут получены данные. Эти параметры принимают либо значение 
`null` - ограничение отсутствует, либо строка вида `2021-01-01 12:00`. Соответственно, если оба параметра равны 
`null` - будут получены все доступные данные.

#### RESPONSE PAYLOAD
TODO

### Получить график истории публикаций за определенный период
**GET** запрос на `/api/{account_internal_id}/toots/graph`
#### REQUEST PAYLOAD
```json
{
  "from": "2021-01-01 12:00",
  "to": null
}
```

Параметры `from` и `to` определяют срок, за который будут получены данные. Эти параметры принимают либо значение 
`null` - ограничение отсутствует, либо строка вида `2021-01-01 12:00`. Соответственно, если оба параметра равны 
`null` - будут получены все доступные данные.

#### RESPONSE PAYLOAD
TODO
