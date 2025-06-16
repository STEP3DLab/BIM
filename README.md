# BIM SaaS Example

## Развертывание

```bash
docker-compose up --build
```

## Пример запроса

```bash
curl -F "file=@scan.laz" http://localhost/api/v1/scan/job
```
