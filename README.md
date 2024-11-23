# RH-marketplace

*  Checko Company Parser

## Local Development

### First Build Only
1. `cp .env.example .env`
2. `docker network create russian-house`
3. `pip install -r requirements/dev.txt`  
4. `docker-compose up -d --build`

### Make migrations
- Create an automatic migration
```shell
alembic revision -m "migration_name" --autogenerate


```
- Run migrations
```shell
alembic upgrade head
```
- Downgrade migrations
```shell
alembic downgrade -1  # or -2 or base or hash of the migration
```

### Access Redis inside container
```shell
docker exec -it app_redis redis-cli -a *redis password*
```
