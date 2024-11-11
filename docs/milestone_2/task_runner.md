# Task runner

As a first choice I used [poetry](https://python-poetry.org/) both as a dependency management system as well as a task runner. However, after some further research, I came across [uv](https://github.com/astral-sh/uv) a python package and project manager written in Rust which is [magnitudes faster]((https://github.com/astral-sh/uv?tab=readme-ov-file#uv)) than poetry. 

Since however, all the documentation and explanations why I chose poetry were already written and committed at this point, I did not want to delete them all, which is why they can be found in the [task_runner_before_migration.md](task_runner_before_migration.md) file.

Most of the plus sides that poetry has also hold up for uv. For example, uv also implements the [PEP Standard](https://peps.python.org/pep-0518/#file-format) of using a [pyproject.toml](../../pyproject.toml). It also makes the project more concise by replacing not only one but multiple config files at once.

The following sections will be quite similar to the ones in [task_runner_before_migration.md](task_runner_before_migration.md) since uv also uses the [pyproject.toml](../../pyproject.toml) file for configuration and can be installed via [pipx](https://github.com/pypa/pipx).

## Initial setup of a task runner (not uv itself)

One key difference is however that uv does not yet support defining tasks, which is technically not possibly with poetry directly either but by installing plugins for poetry. We want to address this missing feature however by using [poethepoet](https://github.com/nat-n/poethepoet) (poe) as a task runner. It was originally created to be used in combination with poetry, however works just as good with uv.

poe is installed using [pipx](https://github.com/pypa/pipx), a tool used to install
Python CLI applications globally while still isolating them in virtual
environments. Once pipx is installed, this is as easy as:
```commandline
pipx install poethepoet
```

Scripts/tasks are easily be declared in a `[tool.poe.tasks]` section of the [pyproject.toml](../../pyproject.toml).

An easy example taken from this projects' [pyproject.toml](../../pyproject.toml) is the following:
```toml
[tool.poe.tasks]
test.help = "Run tests using pytest. Results are found in reports/"
test.cmd = "pytest"
```
This task can now be executed using `poe test` when in the project directory. As can be seen, one can also specify a description of the respective task using `*.help`. This description is shown when running the `poe --help` command.

A more useful and intricate example would be the dev task taken from this projects' pyproject.toml file:
```toml
dev.help = "Start the applicatoin in development mode with reloading enabled"
dev.cmd = "uvicorn app.main:app --reload --log-config log_config.json --reload-dir app"
```
This task would analogously be executed using `poe dev`. More information of poe can be found [here](https://poethepoet.natn.io/).


## Initial setup of uv

uv has an
extensive [documentation](https://docs.astral.sh/uv/) which will
be referenced in the following and explains all the steps for
installing and using Poetry. Poetry is installed also installed using pipx. Having installed pipx, uv can simply be installed by running

```commandline
pipx install uv
```

The most important file when using uv is
the [pyproject.toml](../../pyproject.toml) file in your projects'
repository. It contains all the relevant information for uv and
your project in general. A quick tour of the toml standard can be
found on [the official toml page](https://toml.io/en/).

At the top of the file there is the `[project]` section which
includes basic information about the project:

```toml
[project]
name = "PlantSwap"
version = "0.2.0"
description = "WebApp to swap plants with other people"
authors = ["Raoul Luqué <raoulsluque@gmail.com>"]
readme = "README.md"
requires-python = "<4.0,>=3.11"
packages = [{ include = "app" }]
```

In this section one can also find the dependency list of the project. This includes all project dependencies with their respective version numbers. As explained in the [uv documentation](https://docs.astral.sh/uv/concepts/dependencies/) this list is compliant with the PIP standard for the pyproject.toml file. However, the standard does not support all dependency resolving features that uv can provide (such as dependencies via URLs or GitHub repositories) which is why a second way of declaring dependencies exists. This is explained more thoroughly [here](https://docs.astral.sh/uv/concepts/dependencies/).

In general, poetry can be initialized using
```uv init project-name```. In my case of an existing project, one
can instead use the `uv init` command when in the project
directory to interactively create a pyproject.toml file.

Further dependencies can now be added using

```commandline
uv add dependency-name
```

and

```commandline
uv remove dependency-name
```

respectively. These will automatically be added and removed from the
pyproject.toml file. uv will handle the virtual environment for
you in this case, or you use the existing one if it exists.

In my case of an existing-project which was using poetry, I simply migrated from poetry to uv following the steps explained in this [stackoverflow answer](https://stackoverflow.com/a/79165874/20033036).

