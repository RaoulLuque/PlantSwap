FROM postgres
LABEL authors="raoul"
ENV POSTGRES_PORT 5432
ENV POSTGRES_DB postgres
EXPOSE 5432
USER postgres
