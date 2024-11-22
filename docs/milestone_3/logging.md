# Logging

For logging we chose the native logging options provided by [uvicorn](https://github.com/encode/uvicorn), the framework which runs behind the scenes when using FastAPI. This was due to its ease of use and integration with the existing project.

According to the specifications in the [documentation](https://www.uvicorn.org/settings/#logging), one can specify a log config file. The specifications are explained in a easy to understand and thorough way in [this stackexchange answer](https://stackoverflow.com/a/77007723/20033036). For our project, the logging configuration is specified in [log_config.json](../../log_config.json).

The logging is configured such that all logs are both shown in the command line (which will not be useful to us when deploying the application in the cloud later) and saved to an `app.log` file in a `reports` directory which is created at runtime if it does not exist already.

For uvicorn to retrieve the logging configuration, the logging config file location has to be specified when starting the application. Doing this was as simple as adding another parameter to the poethepoet `poe dev` and `poe deploy` scripts that were set up already. The following is taken from [pyproject.toml](../../pyproject.toml).

```toml
...
[tool.poe.tasks]
...
dev.help = "Start the applicatoin in development mode with reloading enabled and log configuration as specified in log_config.json""
dev.cmd = "uvicorn app.main:app --reload --log-config log_config.json --reload-dir app"
...
deploy.help = "Start the application with reloading disabled and log configuration as specified in log_config.json"
deploy.cmd = "uvicorn app.main:app --log-config log_config.json"
...
```

To override the log level set in the log configuration file, one can also pass `--log-level log-level` to the uvicorn application at start. This integrates great with poethepoet, the task runner, since one can simply write `poe dev --log-level trace` instead of `poe dev` to use the log level trace instead of the default info. The available log levels in decreasing detail of logging are `critical, error, warning, info, debug and trace`.
