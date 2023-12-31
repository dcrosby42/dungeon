# Dungeon 

An overly simple interactive terminal game in Python.  With an overly complicated implementation.

This is more about brushing up on modern Python in 2023, than in creating a great game.

# Usage

Prereqs:
- pyenv
- poetry


```
poetry install
./pytest.sh
./run.sh
```

# Tech Learning Checklist

## Basics

* [ ] modules
  * [ ] __init__
  * [ ] Controlling top-level exports?  Exports from "dir"?
* [ ] pytest
* [ ] type hints
* [ ] __dict__
* [ ] __getattr__

## Advanced

* [ ] generics
* [ ] asyncio - async/await
* [ ] metaclass
* [ ] decorators
* [ ] advanced pytest
  * [ ] BDD / contextual cases?
  * [ ] dynamic test cases?
  * [ ] matchers? hamcrest?

## Tools

* [ ] pyenv
* [ ] black
* [ ] isort
* [ ] poetry
* [ ] pylint
* [ ] mypy
* [ ] pydantic
* [ ] fastapi
* [ ] docker compose
* [ ] SQL Alchemy - ORM and non-ORM
* [ ] boto3 - AWS

# Poetry + Pyenv Rationale

I read [Managing Python Dependencies](https://www.fuzzylabs.ai/blog-post/managing-python-dependencies) and [PyEnv & Poetry - BFFs](https://dev.to/mattcale/pyenv-poetry-bffs-20k6)

According to Fuzzy Labs, Pyenv+Poetry beats venv+pip and Conda in categories "python version mgmt" and "collaboration".

