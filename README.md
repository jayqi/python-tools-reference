# Python Developer Tools Reference

This repository builds the "Python Developer Tools Reference" static website at <https://jayqi.github.io/python-tools-reference/>.

## Requirements

Requires Python 3.11.

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Building the site

To build the site assets to the `site/` directory, run:

```bash
make build
```

## Locking requirements

To make the deployment reproducible, we pin dependencies in a lock file using [pip-tools](https://github.com/jazzband/pip-tools).

The abstract dependencies are specified in [requirements.in](./requirements.in).

To regenerate the lock file, run:

```bash
make lock
```
