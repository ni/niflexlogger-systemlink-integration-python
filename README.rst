===========  ====================================================
Info         NI FlexLogger SystemLink Integration for Python
Author       NI
===========  ====================================================

About
=====
The **niflexlogger-systemlink-integration-python** package contains examples for using Python to
interact with `NI FlexLogger <https://ni.com/flexlogger>`_. The package is
implemented in Python. NI created and supports this package.

Requirements
============
**niflexlogger-systemlink-integration-python** has the following requirements:

* FlexLogger 2020 R3+
* CPython 3.5+

.. _installation_section:

Installation
============
You do not need to install the examples, but you can install all the
dependencies of **niflexlogger-systemlink-integration-python** by downloading the project source and
running this from the project directory::

   $ pip install .

.. _usage_section:

Usage
=====
1. Run the "NI Web Server Configuration" app and configure it for Simple Local
   Access.
2. Start FlexLogger, configure your project to Publish and Consume SystemLink
   Tags, and then close and reopen your project.
3. Run the examples.

The recommended read rate of data using SystemLink tags is 1 Hz. For channels
that require a faster read data rate, consider using the FlexLogger Plugin
Development Kit to create a custom LabVIEW plugin for your project. Refer to
the `Adding a Plugin to Your Project <https://ni.com/documentation/en/flexlogger/latest/manual/adding-a-plugin/>`_
topic for more information.

.. _overview_section:

Examples Overview
=================

* ``systemlink_integration/``

  * ``list_all_tags.py``

    * Get a list of all tags exported by FlexLogger on the local machine.

  * ``start_stop.py``

    * Start and stop a FlexLogger test session.

  * ``create_output_channel.py``

    * Create a FlexLogger output channel and watch for value changes made in the
      FlexLogger GUI.

  * ``simulate_temp_chamber.py``

    * Create FlexLogger channels and write simulated data to them.

.. _support_section:

Support / Feedback
==================
The **niflexlogger-systemlink-integration-python** package is supported by NI. For support for
**niflexlogger-systemlink-integration-python**, open a request through the NI support portal at
`ni.com <https://www.ni.com>`_.

Bugs / Feature Requests
=======================
To report a bug or submit a feature request, use the
`GitHub issues page <https://github.com/ni/niflexlogger-examples-python/issues>`_.

License
=======
**niflexlogger-systemlink-integration-python** is licensed under an MIT-style license (see `LICENSE
<LICENSE>`_).  Other incorporated projects may be licensed under different
licenses. All licenses allow for non-commercial and commercial use.
