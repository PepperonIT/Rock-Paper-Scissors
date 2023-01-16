# Contributing to the project

This guide is intended for developers who want to contribute to the project. It contains information about how to set up the development environment and how to run and/or debug the application in the provided [VS Code dev container](./.devcontainer/README.md).

## Table of contents

- [Contributing to the project](#contributing-to-the-project)
  - [Table of contents](#table-of-contents)
  - [Getting started](#getting-started)
  - [Development](#development)
    - [Environment setup](#environment-setup)
    - [Python modules](#python-modules)
    - [Documentation](#documentation)
      - [Official documentation](#official-documentation)
    - [Debug](#debug)

## Getting started

Contributions are made to this repo via Issues and Pull Requests (PRs). Before you open a new issue or PR, please make sure that you have searched for existing Issues and PRs before creating your own.

## Development

### Environment setup

Follow the steps in the [development container](./.devcontainer/README.md) to set up the development container. The following sections assume that you have set up and are running the development container.

### Python modules

In this project, the Pepper robot is configured as read-only and you are unable to install new Python modules via PyPI (PIP). Therefore you should not modify the `requirements.txt` file.

However, if you need to install a new development dependency, you can add it to the `requirements-dev.txt` file. This file is used to install the development dependencies in the development container and will not be available on the robot. When a new dependency is added to the `requirements-dev.txt` file, you need to rebuild the development container. See the [development container](./.devcontainer/README.md#alternative-1-rebuild-the-container-image) for more information on how to rebuild the dev container.

### Documentation

The documentation for this project is generated using [Sphinx](https://www.sphinx-doc.org/en/master/). To generate the documentation, change directory to `docs/` and run:

```bash
make html
```

The generated documentation is then available in the `docs/build/html/` folder. To view the documentation, open the `index.html` file in a browser.

#### Official documentation

The official documentation for the robot and the NAOqi SDK can be found at [doc.aldebaran.com](http://doc.aldebaran.com/2-5/index.html).

### Debug

To start a debug session, follow the steps below:

1. Open the python file you want to debug.
2. Press <kbd>Ctrl/Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> or <kbd>F1</kbd> and select **Debug: Select and Start Debugging**. Next, select **Python: Debug File** in the dropdown list to start debugging.
