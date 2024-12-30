# Container composition setup

As suggested in the description of the task, Docker (Engine) was used as the container runtime. Our container cluster consists of three containers. One for the application, one for the Postgresql database and a third one for storing the logs of the previous two containers in a redundant manner.

This setup is sufficient for our purposed, however would need to be slightly reconfigured to be able to scale well. A load balancer of sorts would have to be implemented to be able to distribute the load of the application across different instances of the application (containers).

We opted for this cluster setup because it only adds one logging container on top of the necessary containers. Needless to say, splitting the database and application into separate containers leads to more flexibility when possibly changing or migrating the setup in the future and separates business- and database-logic. Therefore, if one of the containers was to fail, the other one would not be affected. Similarly, a higher level of security can be achieved by not exposing the container the database runs on.

## Application container

The dockerfile for the application is explained thoroughly in another [markdown file](dockerfile_in_depth_explanation.md).

## Database container

Since Postgresql was already used previously as the database for our application, containerizing our database was straightforward. Following the [official guide](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/) by docker on how to use the Postgresql docker image, one can get up and running relatively quickly.

The following shows the section of the [docker-compose.yml](../../docker-compose.yml) corresponding to the postgresql container.

```yaml
  plantswap-postgres:
    image: "postgres:latest"
    container_name: plantswap-postgres
    restart: always
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - PGUSER=${POSTGRES_USER}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    # Log all Queries in a file
    command: [ "postgres", "-c", "logging_collector=on", "-c", "log_statement=all" ]
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready", "-d", "db_prod" ]
      interval: 30s
      timeout: 60s
      retries: 5
      start_period: 80s
```

As described in the above resource on how to use postgresql with docker, we use the official postgresql (base) image. To persistently store the database entries even if the database container may crash, or we want to restart the containers, we use a docker volume to store the database files. We map the postgres ports to the default `5432`. Since we use environment variables to set the secrets of our application, we reuse these to set the respective values of the database. The (entry) command of the container is slightly altered to redirect the logs of the database to a file which is then synchronized with the logging container using the docker volume. To only start our application after the database has successfully started, we use a health check to check whether the database is ready to receive requests. For more information on safe database health checks, see [this resource](https://github.com/peter-evans/docker-compose-healthcheck).

## Logging container

For the (base) image of the logging container, we could have gone for a very lightweight image since we basically only need storage and no other capabilities. However, we instead chose an image which would enable us to possibly sync our backups/logs to any other SSH compatible service like S3, Azure or Dropbox. This image is namely [offen/docker-volume-backup](https://hub.docker.com/r/offen/docker-volume-backup). The section of the [docker-compose.yml](../../docker-compose.yml) for the logging container therefore looks as follows:

```yaml
  plantswap-logging:
    image: "offen/docker-volume-backup:latest"
    container_name: plantswap-logging
    restart: always
    volumes:
      - postgres-data:/var/lib/backup/database_data_and_logs
      - app-logs:/var/lib/backup/application_logs
```

The configuration is self-explanatory as we simply sync the logs and database via the volumes.
