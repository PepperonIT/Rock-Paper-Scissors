# Development Container

This repository includes configuration for a local development container based on [Visual Studio Code Remote - Containers](https://aka.ms/vscode-remote/containers). This allows you to open the repository in a container running on your local machine, and take advantage of the tools and extensions installed in the container.

## Usage

1. Install Docker Desktop or Docker for Linux on your local machine. (See [docs](https://aka.ms/vscode-remote/containers/getting-started) for additional details.)

2. Install [Visual Studio Code](https://code.visualstudio.com/) and the [Dev Containers](https://aka.ms/vscode-remote/download/containers) extension.

3. Clone this repository to your local machine and open it in Visual Studio Code.

4. Press <kbd>Ctrl/Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> or <kbd>F1</kbd> and select **Dev Containers: Open Folder in Container...**.  
*NOTE: This step may take a while the first time you run it.*

### Improved disk I/O

For better disk I/O on macOS and Windows, use the **Dev Containers: Clone Repository in Container Volume...** command to create a container with a Docker volume attached. IMPORTANT: This will not preserve any local changes not committed and pushed to the remote repository when the container is deleted.

## Common issues

### Cannot start the devlopement container

Make sure that Docker Desktop is running, and that you have the latest version of the [Dev Containers](https://aka.ms/vscode-remote/download/containers) extension installed.

### Unable to build the container image

#### Alternative 1: Rebuild the container image

Press <kbd>Ctrl/Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> or <kbd>F1</kbd> and select **Dev Containers: Rebuild Without Cache and Reopen in Container**.

This will rebuild the container image without using the cache and then reopen the folder in the container.

#### Alternative 2: Manually rebuild the container image

1. Open a terminal in the cloned repository folder.

2. Run the following command to build the container image:

```bash
cd .devcontainer && docker build .
```

3. Press <kbd>Ctrl/Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> or <kbd>F1</kbd> and select **Dev Containers: Open Folder in Container...**.

### Unable to use a certain Python module or Python tool

If a new Python module or tool is added to the any of the requirement files (`requirements.txt` and `requirements-dev.txt`) or a expected tool is missing, you need to rebuild the development container. See [rebuild the container image](./.devcontainer/README.md#alternative-1-rebuild-the-container-image) for more information on how to rebuild the dev container.
