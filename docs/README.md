[**This page is also available in english**](/docs/README_EN.md)

# Mastodon meter

Mastodon meter - это открытая система аналитики для федеративной [социальной сети Mastodon](https://joinmastodon.org).

### Возможности Mastodon meter:

- Добавлять и удалять аккаунты в список отслеживаемых;
- По расписанию (по умолчанию ежедневно) производить измерения для каждого из отслеживаемых аккаунтов:
  получать счетчик подписчиков и статусов и записывать их в базу данных;
- На основании полученных данных генерировать графики и текстовые отчеты;
- Предоставляет удобный API интерфейс для использования в ваших собственных проектах, в т.ч. для получения "сырых"
  данных для последующей самостоятельной обработки;

### Преимущества Mastodon meter:

- **Легкий и быстрый**. Mastodon meter использует современный асинхронный веб-фреймворк FastAPI, асинхронные библиотеки
  Motor и HttpX. Благодаря этому он работает быстро при минимальном потреблении ресурсов (в несколько раз быстрее по
  сравнению с синхронными альтернативами);
- **Производительный**. Благодаря используемым технологиям сервер может работать с сотнями или тысячами отслеживаемых
  аккаунтов без существенной потери производительности. Масштабируемость заложена в архитектуру решения;
- **Современные технологии**. В основе решения лежат современные библиотеки FastAPI и HttpX, нереляционная БД MongoDB,
  асинхронный стиль программирования. Для менеджмента зависимостей используется Poetry, для логгирования - Loguru;
- **Легкая поддержка**. Вся кодовая база соответствует стандартам PEP8, повсеместно используются аннотации типов. Такой
  код проще поддерживать и развивать совместно с другими разработчиками. Аннотации типов также позволяют широко
  применять статический анализ, что снижает количество ошибок и повышает качество кода;
- **Надежность**. Благодаря валидации входящих и исходящих запросов через Pydantic API трудно "положить" невалидными
  запросами.

### Применяемые технологии:

- Асинхронный веб-фреймворк **FastAPI**;
- Система валидации **Pydantic**;
- Асинхронная библиотека для работы с HTTP запросами **HttpX**;
- Библиотека для логгирования **Loguru**;
- Нереляционная база данных **MongoDB**;
- Асинхронный клиент для MongoDB **Motor**;
- Генерация графиков - **Matplotlib**;
- ASGI сервер **Uvicorn**;
- Статический анализ, форматирование, линтеринг: **Mypy, Black, Flake8**.

### Установка и запуск

1. Уставить Poetry следуя официальной [инструкции](https://python-poetry.org/docs/):
   `$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

2. Клонировать репозиторий и перейти в папку с ним: `$ git clone https://github.com/arseniiarsenii/mastodon-meter.git
   && cd mastodon-meter`

3. Установить зависимости в виртуальное окружение с помощью Poetry и перейти в
   него: `$ poetry install --no-dev && poetry shell`

4. Экспортировать [адрес подключения](https://docs.mongodb.com/guides/server/drivers/) к базе MongoDB в переменные
   окружения: `$ export MONGO_CONNECTION_URL="mongodb+srv://your_connection_string_here"`

5. Перейти в директорию с исходным кодом и запустить сервер: `$ cd src && uvicorn app:app`

Сервер запущен и работает по адресу `http://127.0.0.1:8000`.

### Разработка

Вы можете принять участие в разработке Mastodon-meter. Для этого сделайте fork этого репозитория, внесите изменения и
отправьте pull request.

Данное решение распространяется под лицензией [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html). Использование
в коммерческих целях, а также сокрытие кода не допускаются.

---

# Документация API

## Операции со списком отслеживаемых аккаунтов

### Добавить аккаунт в список отслеживаемых

**POST** запрос на `/api/accounts/add`

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

### Получить список отслеживаемых аккаунтов

**GET** запрос на `/api/accounts/tracked`

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

### Собрать данные для всех отслеживаемых аккаунтов и записать в БД

**GET** запрос на `/api/gather-data`

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

## Операции с аккаунтами из списка отслеживаемых

### Получить сырые данные за определенный период

**GET** запрос на `/api/{account_internal_id}/data`

#### REQUEST PAYLOAD

```json
{
  "since": "2021-01-01 12:00",
  "to": null
}
```

Параметры `since` и `to` определяют срок, за который будут получены данные. Эти параметры принимают либо значение
`null` - ограничение отсутствует, либо строка вида `2021-01-01 12:00`. Соответственно, если оба параметра равны
`null` - будут получены все доступные данные.

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

### Получить график истории подписчиков за определенный период

**GET** запрос на `/api/{account_internal_id}/graph/subscribers`

#### REQUEST PAYLOAD

```json
{
  "since": "2021-01-01 12:00",
  "to": null
}
```

Параметры `since` и `to` определяют срок, за который будут получены данные. Эти параметры принимают либо значение
`null` - ограничение отсутствует, либо строка вида `2021-01-01 12:00`. Соответственно, если оба параметра равны
`null` - будут получены все доступные данные.

#### RESPONSE PAYLOAD

Success:
Файл с расширением `.png`

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Получить график истории публикаций за определенный период

**GET** запрос на `/api/{account_internal_id}/graph/toots`

#### REQUEST PAYLOAD

```json
{
  "since": "2021-01-01 12:00",
  "to": null
}
```

Параметры `since` и `to` определяют срок, за который будут получены данные. Эти параметры принимают либо значение
`null` - ограничение отсутствует, либо строка вида `2021-01-01 12:00`. Соответственно, если оба параметра равны
`null` - будут получены все доступные данные.

#### RESPONSE PAYLOAD

Success:
Файл с расширением `.png`

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Получить общий график истории публикаций и подписчиков за определенный период

**GET** запрос на `/api/{account_internal_id}/graph/common`

#### REQUEST PAYLOAD

```json
{
  "since": "2021-01-01 12:00",
  "to": null
}
```

Параметры `since` и `to` определяют срок, за который будут получены данные. Эти параметры принимают либо значение
`null` - ограничение отсутствует, либо строка вида `2021-01-01 12:00`. Соответственно, если оба параметра равны
`null` - будут получены все доступные данные.

#### RESPONSE PAYLOAD

Success:
Файл с расширением `.png`

Error:

```json
{
  "status": false,
  "message": "Description for the operation result"
}
```

### Получить простой текстовый отчет по отслеживаемым аккаунтам

Возвращает текстовый отчет вида:

```
Mastodon-meter summary report generated on 2021.09.01 09:00 UTC

account_name_1@mastodon.social: 102 subscribers, 2000 (+2) statuses
account_name_2@mastodon.social: 94 subscribers, 735 statuses
account_name_3@mastodon.social: 39 subscribers, 4671 (+5) statuses
...
account_name_n@mastodon.social: 45 subscribers, 118 statuses
```

Такой отчет удобно вставить в сообщение м отправить через бота или по почте.

**GET** запрос на `/api/{account_internal_id}/graph/common`

#### REQUEST PAYLOAD

В поле `accounts` необходимо указывать список внутренних идентификаторов аккаунтов, которые будут включены в отчет

```json
{
  "accounts": [
    "001a24eb90864bf2ba046f36f74f3a8a",
    "0ffc53bbeca947f69536f141f2df20cf",
    "da20f348160b418aa5d158baade0d366"
  ]
}
```

Если полю присвоить значение `null` - отчет будет составлен для всех отслеживаемых аккаунтов

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
