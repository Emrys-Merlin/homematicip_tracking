====================
HomematicIP Tracking
====================

Track the temperature and humidity of a HomematicIP smart home and expose them as prometheus metrics


* Free software: MIT license


Installation
------------
So far this project only exists on github and you can simply clone and install it as follows:

.. code-block:: Shell

   git clone git@github.com:Emrys-Merlin/homematicip_tracking.git
   cd homematic_tracking
   pip install -r requirements.txt
   pip install -e .


Usage
-----

* The above installation gives you access to the shell command `homematicip_tracking` which polls the HomematicIP sensors and exposes the metrics.

.. code-block:: Shell

   homematicip_tracking <config> <port> [<options>]

* `<config>` should point to the config file for the HomematicIP API access. This file can be generated using the `hmip_generate_auth_token.py` of the homematic package found at `https://github.com/coreGreenberet/homematicip-rest-api`.
* `<port>` the port at which the prometheus metrics will be exposed
* At the moment there are two possible options `--wait` is the waiting time between HomematicIP polls and `--print/--no-print` which prints the read sensor data to stdout.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
