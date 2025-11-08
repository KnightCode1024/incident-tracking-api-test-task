# incident-tracking-api-test-task
Тестовое задание.  Задача: разработать API-сервис для учёта инцидентов.

## Связь со мной
- [Телеграм](https://t.me/ProstoKiReal)

## Технологии
 - `Python`
 - `Postgres`
 - `Django` `DRF`
 - `Docker`
 - `Git`

## Запуск

1) Создайте `.env` на основе `.env.example`
2) Вставте секретный ключ 
```bash
# Генерация ключа
openssl rand -hex 32
```
3) Запустите Docker контейнеры
```bash
docker-compose up --build -d
```
При запуски контейнеров автоматически подгружаются тестовые данные из фикстуры. Для доступа в админку пароль и логин - `root`

## Эндпоинты

Вы можете импортировать `postman.json` в Postman чтобы протестировать результат.

### Метаданные системы 
Получить список всех статусов и источников
```text
GET http://localhost:8000/api/incidents/metadata/
```

### Создать инцидент
```text
POST http://localhost:8000/api/incidents/
Content-Type: application/json
```
```json
{
    "description": "Текст проблемы",
    "source_code": "operator"
}
```
### Получить все инциденты
```text
GET http://localhost:8000/api/incidents/
```

### Получить инцидент по ID
```text
GET http://localhost:8000/api/incidents/1/
```

### Обновить статус инцидента
```text
PATCH http://localhost:8000/api/incidents/1/status/
Content-Type: application/json
```

```json
{
    "status_code": "open|in_work|close"
}
```

### Фильтрация инцидентов
```text
GET http://localhost:8000/api/incidents/?status=open
GET http://localhost:8000/api/incidents/?source=monitoring
GET http://localhost:8000/api/incidents/?status=open&source=operator
```
