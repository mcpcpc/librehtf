# LibreHTF

An open hardware test framework.

## Install

### PyPI

Install and update using pip:

```shell
pip install -U librehtf
```

### Repository

When using git, clone the repository and change your present working directory.

```shell
git clone http://github.com/mcpcpc/librehtf
cd librehtf/
```

Create and activate a virtual environment.

```shell
python3 -m venv venv
source venv/bin/activate
```

Install LibreHTF to the virtual environment.

```shell
pip install -e .
```

## Commands

### db-init

The Sqlite3 database can be initialized or re-initialized with the
following command.

```shell
flask --app librehtf init-db
```

## Deployment

Before deployment, we *strongly* encourage you to override the
default `SECRET_KEY` variable. This can be done by creating a
`conf.py` file and placing it in the same root as the instance (i.e. typically where the SQLite database resides).

```python
SECRET_KEY = “192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf“
```

There are a number of ways to generate a secret key value. The
simplest would be to use the built-in secrets Python library.

```shell
$ python -c ‘import secrets; print(secrets.token_hex())’
‘192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf’
```

### Waitress

Production WSGI via waitress.

```shell
pip install waitress
waitress-serve --call librehtf:create_app
```

## Test

```shell
python3 -m unittest
```

Run with coverage report.

```shell
coverage run -m unittest
coverage report
coverage html  # open htmlcov/index.html in a browser
```

## Authorization

OpenHTF provides a simple role-based access control (RBAC) for protecting both APIs and environment configuration. There are three levels of user access controls: administrator, functional and public. Responsibilities range from least restrictive to most restrictive, respectively.

| Function      | Description                                                         | Evaluation | API Access | Management |
|---------------|---------------------------------------------------------------------|------------|------------|------------|
| Administrator | An individual for system administration and user management.        | Yes        | Yes        | Yes        |
| Functional    | A non-human interface, typically for machine integration.           | Yes        | Yes        | Limited    |
| Public        | Typically an operator or technician responsible for test execution. | Yes        | No         | No         |

## Nomenclature 

OpenHTF is architected to allow inherent branching of tests.  At the core, there are three tiers of organization: device, test and task.

### Device

Devices refer to specific to hardware versions or product configurations. These are typically descriptive in nature and are useful when organizing hardware test interfaces that are intended to be used with multiple product offerings. Each device may have one or multiple *test* configurations. 

### Test

Tests are a collection of similar or related tasks. Thus, executing a test will execute all collected task operators.

### Task

The smallest unitdiscretized observation for a given test. The result of running a task can either be informative or comparative. When comparing the result of a task, the resulting outcome either yields PASS or FAIL.
