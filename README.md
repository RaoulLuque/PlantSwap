# PlantSwap

![Logo created using Dall-E](docs/milestone_1/logo.webp)

[![tests](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FRaoulLuque%2F5d6fa85dbeff94c59c734a06a656267f%2Fraw%2FPlantSwap-junit-tests.json&style=flat
)](https://github.com/RaoulLuque/PlantSwap/actions)
[![coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FRaoulLuque%2F5d6fa85dbeff94c59c734a06a656267f%2Fraw%2FPlantSwap-cobertura-coverage.json&style=flat
)](https://github.com/RaoulLuque/PlantSwap/actions)

PlantSwap is an application which enables you to trade your plant
offsets for other plants of your liking.

You can either find a person which wants to trade their plant for your
plant directly or sell your plants on the platform
to receive coins which you can then use the buy plants from other
people.

This repository documents the progress in the cloud computing course I
took part in at the Universidad de Granada for my masters.

The above logo was generated
using [Dall-E](https://openai.com/index/dall-e/).

# Starting up the application

## Prerequisites
The project needs a Postgresql database to be running to be able to use all functionalities. Using a .env file one can pass the application the necessary details of the database. The specific parameters to be set are found in [config.py](app/core/config.py).

## Using poetry
To start up the application, one will have to install the dependencies first. [Poetry](https://python-poetry.org/) is recommended to be installed. An installation guide can be found [here](https://python-poetry.org/docs/#installation).

After having installed poetry, to install the dependencies run
````commandline
poetry install
````
This will install all dependencies and the project can be started using
```commandline
poetry run fastapi dev
```
to use development mode and
```commandline
poetry run fastapi run
```
to use release mode.

By default, the api will be served at `http://0.0.0.0:8000 `.

## Using pip
Alternatively, the dependencies can be installed using pip. Note that it is recommended to have set up a virtual environment beforehand in this case. To install the dependencies simply run
````commandline
pip install .
````
This will install all dependencies and the project can be started using
```commandline
fastapi dev
```
to use development mode and
```commandline
fastapi run
```
to use release mode.

By default, the api will be served at `http://0.0.0.0:8000 `.
# General development progress of the app

The following list keeps track of the development progress of the app
and its backend/API.

## [Basic functionality](https://github.com/RaoulLuque/PlantSwap/milestone/2)

Basic functionality includes things such as:

- [x] [Setup of API without functionality](https://github.com/RaoulLuque/PlantSwap/issues/4)
- [x] [Create (secure) login functionality for administrators](https://github.com/RaoulLuque/PlantSwap/issues/6)
- [x] [Create (secure) login functionality for users](https://github.com/RaoulLuque/PlantSwap/issues/5)
- [x] [Add option for users to create accounts](https://github.com/RaoulLuque/PlantSwap/issues/10)
- [ ] [Add option for users to create ads for their plants](https://github.com/RaoulLuque/PlantSwap/issues/7)
- [ ] [Administrators should be able to delete ads of users](https://github.com/RaoulLuque/PlantSwap/issues/8)

# Milestones

The following are references to the tasks of the respective milestones
as discussed in
the [Repository](https://github.com/cvillalonga/CC-24-25) of the cloud
computing class.

## [Milestone 1](https://github.com/RaoulLuque/PlantSwap/milestone/1)

- 🔧 [Configuration of Git and GitHub](docs/milestone_1/github_configuration.md)
- 📖 [Description of the problem and the application to solve it](docs/milestone_1/problem_description.md)
- ⚖️ [MIT License used for the project](LICENSE)

## Milestone 2

- ...

