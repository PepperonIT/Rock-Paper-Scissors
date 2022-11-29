This is a repo for the rock-paper-scissor module.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   autoapi/index

Usage
=====

If you are not using the development container, you will need to install the required dependencies first. Otherwise you can skip to step 4.

**Step 1.** Install [Python 2.7](https://www.python.org/download/releases/2.7/).

**Step 2.** Start by installing the required modules

```bash
pip install -r requirements.txt
```

**Step 3.** Download and extract the [Pepper SDK](PepperSDK.md).

**Step 4.** Upload the [`images`](./images/) folder to pepper. Use the path `/data/home/nao/pepperonit/rps/images`, e.g. `/data/home/nao/pepperonit/rps/images/RPS_rock.jpg`.

**Step 5.** Start the application with `python ./src/app.py`.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
