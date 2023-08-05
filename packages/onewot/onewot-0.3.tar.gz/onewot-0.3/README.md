<h1 align="center">Onewot</h1>
<p>
An opinionated, static typed WotBlitz API wrapper for Python3.

Python >=3.6 are currently supported.
</p>

## Installation
Install Onewot from PyPi with the following command:

```bash
python -m pip install -U onewot
# Windows users may need to use this instead...
py -3 -m pip install -U onewot
```

----

## Start up client

```py
import onewot
client = onewot.WOTBClient(application="...")
```

----

## Example

```py
import onewot
client = onewot.WOTBClient(application="...")
print(client.fetch_user(152870490))
```

----

## Documentation

Coming soon...

----

## Python optimization flags
CPython provides two optimisation flags that remove internal safety checks that are useful for development, and change other internal settings in the interpreter.

- python main.py - no optimisation - this is the default.
- python -O main.py - first level optimisation - features such as internal
    assertions will be disabled.
- python -OO main.py - second level optimisation - more features (**including
    all docstrings**) will be removed from the loaded code at runtime.

**A minimum of first level of optimizations** is recommended when running applications in a production environment.