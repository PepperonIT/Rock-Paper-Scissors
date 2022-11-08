# Rock-Paper-Scissors

This is a repo for the rock-paper-scissor module.

## Usage

If you are not using the development container, you will need to install the required dependencies first. Otherwise you can skip to step 4.

**Step 1.** Install [Python 2.7](https://www.python.org/download/releases/2.7/).

**Step 2.** Start by installing the required modules

```bash
pip install -r requirements.txt
```

**Step 3.** Download and extract the [Pepper SDK](PepperSDK.md).

**Step 4.** Start the application with `python ./src/app.py`

## Capture images

To capture images, you need to run the `capture.py` script. This script will capture images from the robot's camera and save them on the computer the script is running on. If you are using the dev container and not already in the project root, navigate to `/workspaces/Rock-Paper-Scissors`. Next run

```bash
python ./src/ai/capture_image.py [name_of_image.jpg]
```

If only an image name is provided, the image will be saved in the current path. If a path is provided, the image will be saved in the specified path.

## Development

### Dependencies

All dependencies are managed by pip and are listed in the `requirements.txt` and `requirements-dev.txt` file. The development dependencies are only required if you want to make changes to the code. To install the dependencies, including the development dependencies, run:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

The `requirements.txt` file contains the dependencies required to launch the application and the `requirements-dev.txt` file contains tools used during development.

If a new dependency is added, make sure to update the correct requirement file with name and version of the new dependency. The same applies when removing a dependency. To automatically update the requirements file `requirements.txt`, run:

```bash
pipreqs
```

### Development Container _(optional)_

This repository includes a Visual Studio Code Dev Containers / GitHub Codespaces development container.

- For [Dev Containers](https://aka.ms/vscode-remote/download/containers), use the **Dev Containers: Clone Repository in Container Volume...** command which creates a Docker volume for better disk I/O on macOS and Windows.
  - If you already have VS Code and Docker installed, you can also click [here](vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/D7017E/Rock-Paper-Scissors) to get started. This will cause VS Code to automatically install the Dev Containers extension if needed, clone the source code into a container volume, and spin up a dev container for use.
- For Codespaces, install the [GitHub Codespaces](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces) extension in VS Code, and use the **Codespaces: Create New Codespace** command.

See the [development container README](.devcontainer/README.md) for more information.

### Debug

To start a debug session, the [debugpy](https://pypi.org/project/debugpy/) module must be installed in the environment, see [Dependencies](#dependencies).

#### Using VS Code

1. Open the python file you want to debug.
2. Press <kbd>Ctrl/Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> or <kbd>F1</kbd> and select **Debug: Select and Start Debugging**. Next, select **Python: Debug File** in the dropdown list to start debugging.
