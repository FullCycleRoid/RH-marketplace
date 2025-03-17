# RH Backend


### Swagger
* https://localhost:8000/marketplace/docs

### First Build Only
1. `cp .env.example .env`
2. `docker network create rh`

### Local launch:
1. `docker compose up --build`
2. `alembic upgrade head`
3. run app from IDE using:
   1) `src/main.py` file as script path;
   2) Project's root dir as working directory;
   3) Path to `.env.local` file for .env path field.

### Linters
Format the code with `ruff --fix` and `ruff format`
```shell
sudo docker compose exec app format
```

### Make migrations
- Create an automatic migration
```shell
migrations revision -m "migration_name" --autogenerate


```
- Run migrations
```shell
migrations upgrade head
```
- Downgrade migrations
```shell
migrations downgrade -1  # or -2 or base or hash of the migration
```

### Access Redis inside container
```shell
docker exec -it app_redis redis-cli -a *redis password*
```

### Tests
All tests are integrational and require DB connection. 

One of the choices I've made is to use default database (`postgres`), separated from app's `app` database.
- Using default database makes it easier to run tests in CI/CD environments, since there is no need to setup additional databases
- Tests are run with upgrading & downgrading alembic migrations. It's not perfect, but works fine. 

Run tests
```shell
pytest -v
```
### Justfile
The template is using [Just](https://github.com/casey/just). 

It's a Makefile alternative written in Rust with a nice syntax.

You can find all the shortcuts in `justfile` or run the following command to list them all:
```shell
just --list
```
Info about installation can be found [here](https://github.com/casey/just#packages).
### Backup and Restore database
We are using `pg_dump` and `pg_restore` to backup and restore the database.
- Backup
```shell
just backup
# output example
Backup process started.
Backup has been created and saved to /backups/backup-year-month-date-HHMMSS.dump.gz
```

- Copy the backup file or a directory with all backups to your local machine
```shell
just mount-docker-backup  # get all backups
just mount-docker-backup backup-year-month-date-HHMMSS.dump.gz  # get a specific backup
```
- Restore
```shell
just restore backup-year-month-date-HHMMSS.dump.gz
# output example
Dropping the database...
Creating a new database...
Applying the backup to the new database...
Backup applied successfully.
```
