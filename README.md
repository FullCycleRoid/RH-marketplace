# RH-marketplace

*  Checko Company Parser

## Local Development

### First Build Only
1. `cp .env.example .env`
2. `docker network create russian-house`
3. `docker-compose up -d --build`

### Linters
Format the code with `ruff --fix` and `ruff format`
```shell
sudo docker compose exec app format
```

### Migrations
- Create an automatic migration from changes in `src/database.py`
```shell
sudo docker compose exec app makemigrations *migration_name*

```
- Run migrations
```shell
sudo docker compose exec app migrate
```
- Downgrade migrations
```shell
sudo docker compose exec app downgrade -1
```