# Rock-Paper-Scissors

This is a repo for the rock-paper-scissor module to make the robot [Pepper](https://www.aldebaran.com/en/pepper) play a game of rock paper scissors with a human opponent. The module is written in Python 2.7 and uses the [NAOqi python SDK](http://doc.aldebaran.com/2-5/dev/python/) to communicate with the robot.

## Tools / Installation

The following tools are required to install and run the application:

- SSH client ([PuTTY](https://www.putty.org/), [OpenSSH](https://www.openssh.com/), etc.)
- SFTP client ([FileZilla](https://filezilla-project.org/), [OpenSSH](https://www.openssh.com/), etc.)

These tools are used to connect to the robot and transfer the application files to the robot. Instructions are provided below on how to install the application on the robot. This section will not cover how to run the application on your local machine.

### Installation

To install the application, follow these steps:

1. Connect to the robot using SFTP.

2. Transfer the `src` folder to the robot using the path `~/rps/src`.

3. Transfer the `www/rps` folder to the robot using the path `~/.local/share/ota/rps`.

## Usage

1. Connect to the robot using SSH.

2. Run the below command to start the application. Replace `<LANGUAGE>` with the language you want to use: `English` or `Swedish`.

    ```bash
    python ./rps/src/app.py <LANGUAGE>
    ```

    Pepper will then start the application and wait for a human opponent to join the game.

### Examples

Start the application in English:

```bash
python ./rps/src/app.py English
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to set up the development environment on your local machine and how to suggest changes or enhancements to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
