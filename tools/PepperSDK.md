# Instructions for installing the Pepper SDK

*The following instructions are for installing the Pepper SDK on a Linux machine.*

**Step 1.** Download the [Pepper SDK](https://community-static.aldebaran.com/resources/2.5.10/Python%20SDK/pynaoqi-python2.7-2.5.7.1-linux64.tar.gz) and extract it:

```sh
tar -xf path/to/downloaded/sdk -C ~/lib/python2
```

**Step 2.** Add the package to your pythonpath. If you are using bash, add the following line to your `~/.bashrc` file:

```sh
export PYTHONPATH=${PYTHONPATH}:/path/to/sdk
```

Example:

```sh
export PYTHONPATH=${PYTHONPATH}:/home/myusername/lib/python2/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages
```

**Step 3.** You can now import the package in your python code. To verify that the installation was successful, follow the instructions in the next section.

## Verify installation

To verify the installation of noaqi, you can run:

```python
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "<IP-Address-to-pepper>", 9559) # LTU Pepper: 130.240.238.32
tts.say("Hello, world!")
```
