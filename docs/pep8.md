# PEP8 Formatting

## What is PEP8?

> PEP8 is a style guide for Python code. It is a set of rules for writing Python code that is readable by humans.

## Verify your code

### Requirements

- Install Flake8

```terminal
user@server:$ pip install flake8
```

### Command

```terminal
user@server:~/ flake8 --exclude=.git,.venv,env,.tox,dist,doc,*egg,build,.vscode,*migrations/*.py,*/local_settings.py .

```

### Using Flake8 with docker-compose

```terminal
user@server:$ docker-compose run web flake8 --exclude=.git,.venv,env,.tox,dist,doc,*egg,build,.vscode,*migrations/*.py,*/local_settings.py .
```
