# Compose file in-depth explanation

We have already discussed some details of the [docker-compose.yml](../../docker-compose.yml) file in the [explanation of the container composition setup](01_container_composition_setup.md). More precisely, we have discussed the general structure of using three containers, the setup of the database and the logging container, respectively. Therefore, we only need to take a brief look at the application container's section in the compose file.

The following is the respective section:
```yaml
  plantswap-app:
    build: .
    container_name: plantswap-app
    restart: always
    environment:
      - POSTGRES_SERVER=plantswap-postgres
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - SECRET_KEY=${SECRET_KEY}
      - FIRST_SUPERUSER=${FIRST_SUPERUSER}
      - FIRST_SUPERUSER_PASSWORD=${FIRST_SUPERUSER_PASSWORD}
    ports:
      - "8000:8000"
    volumes:
      - app-logs:/PlantSwap/reports
    depends_on:
      plantswap-postgres:
        condition: service_healthy
    links:
      - plantswap-postgres
```
As a (base) image, we use this project's [Dockerfile](../../Dockerfile) and only provide the necessary environment variables. Furthermore, we expose the necessary ports and set a volume to sync the logs of the application. As mentioned in the [explanation of the container composition setup](01_container_composition_setup.md), the application depends on the existence/healthiness of the postgres instance, which is why it will only start once the postgres container is healthy. At last, we create a link to the postgres container for them to be able to communicate.
