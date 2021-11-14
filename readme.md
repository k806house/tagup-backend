# TagUp

Команда [k806](https://k806.ru/)

## Пререквизиты

- git-lfs/3.0.2
- Docker version 20.10.6
- docker-compose version 1.29.1

## Запуск

```bash
./run_dev
```

Сервер будет доступен по `localhost:8080`.

## API

### Request

`GET /tags&query="<query>"`

### Response

    {
        "status":"ok",
        "data":[
        {
            "tag":"сапоги",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"ботинки осенние",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"кроссовки",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"ботинки зимние",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"полусапожки",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"ботинки челси",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"кеды",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"ортопедическая обувь",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"обувь",
            "isRouting":false,
            "ref":""
        },
        {
            "tag":"туфли",
            "isRouting":false,
            "ref":""
        }
    ]}

## Фронт

[tagup-frontend](https://github.com/k806house/tagup-frontend)
