# Task runner

As a task runner I chose [Poetry](https://python-poetry.org/). First
and foremost because it implements
the [PEP Standard](https://peps.python.org/pep-0518/#file-format) of
using a [pyproject.toml](../../pyproject.toml) file for configuration
of the project and dependencies. Using this pyproject.toml file,
Poetry handles all dependency management, therefore replacing pip. Not
only does the pyproject.toml file therefore replace the
requirements.txt, but also pytest.cfg, setup.py and similar files.
While doing this, Poetry also warns more consistently if dependency
conflicts exist.

The above however is not actually the task runner part of Poetry. In
addition to the aforementioned, one can also
define [custom scripts](https://python-poetry.org/docs/pyproject/#scripts),
i.e. CLI commands which will then execute arbitrary python functions
in the project directory. These can then be arbitrary command line
calls which can standardize the execution of tests or the build
pipeline.

At last, Poetry shows some similarity to Cargo, the native package
manager and task runner of the Rust Programming Language, which I am
personally quite accustomed to.

## Initial setup of Poetry

Poetry has an
extensive [documentation](https://python-poetry.org/docs/) which will
be referenced in the following and explains all the steps for
installing and using Poetry. Poetry is installed
using [pipx](https://github.com/pypa/pipx), a tool used to install
Python CLI applications globally while still isolating them in virtual
environments.

Having installed pipx, Poetry can simply be installed by running

```commandline
pipx install poetry
```

The most important file when using Poetry is
the [pyproject.toml](../../pyproject.toml) file in your projects
repository. It contains all the relevant information for Poetry and
your project in general. A quick tour of the toml standard can be
found on [the official toml page](https://toml.io/en/).

At the top of the file there is the `[tool.poetry]` section which
includes basic information about the project:

```toml
[tool.poetry]
name = "PlantSwap"
version = "0.1.0"
description = "WebApp to swap plants with other people"
authors = ["Raoul Luqué <raoulsluque@gmail.com>"]
readme = "README.md"
packages = [{ include = "app" }]
```

A few configuration sections for testing follow whereas at the end of
the file, the dependency list of the project is found in the
`[tool.poetry.dependencies]`´ section.

In general, poetry can be initialized using
```poetry init project-name```. In my case of an existing project, one
can instead use the `poetry init` command when in the project
directory to interactively create a pyproject.toml file.

Further dependencies can now be added using

```commandline
poetry add dependency-name
```

and

```commandline
poetry remove dependency-name
```

respectively. These will automatically be added and removed from the
pyproject.toml file. Poetry will handle the virtual environment for
you in this case, or you use the existing one if it exists.

In my case of an existing-project with existing dependencies and
virtual environment, I simply added all my dependencies from the
existing requirements.txt by running

```commandline
poetry add $(cat requirements.txt)
```

This and other solutions to this problem of injecting an existing
requirements.txt file into Poetry can be found
in [this](https://stackoverflow.com/questions/62764148/how-to-import-an-existing-requirements-txt-into-a-poetry-project)
stackoverflow post.

A possibly interesting configuration that can be done is setting the
virtual environment location to be in-project. I.e. telling poetry to
create a venv file in the project directory and not in another cache
directory. This has the plus side of making it more compatible with
other tools and avoiding to forget to delete the venv directory when
deleting the project, but has the possible downside not being able to
have multiple virtual environments for one project which is otherwise
possible with poetry. The command to change this setting is:

```commandline
poetry config virtualenvs.in-project true
```

## Using Poetry

If another person would now want to use the project they could simply
use the

```commandline
poetry install
```

command to install all dependencies in a virtual environment managed
by Poetry (supposing Poetry is installed on their machine).

Not only will Poetry manage the dependencies and setup of test tools
but also allow for creation of scripts that can streamline execution
of projects and running tests. Since our project has not grown to a
scope where this feature is necessary, no scripts have been defined
yet, however the documentation for doing so can be
found [here](https://python-poetry.org/docs/pyproject/#scripts).

So far, for starting the app one can simply run

```commandline
poetry run fastapi dev
```

and

```commandline
poetry run fastapi run
```

to run the application and development and production mode,
respectively.

To execute the tests one can simply run

```commandline
poetry run pytest
```

For more information on the test framework used,
see [test_framework_and_assertion_library.md](testing_framework_and_assertion_library.md).

