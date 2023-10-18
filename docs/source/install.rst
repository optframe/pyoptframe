Installation
=============

OptFrame Python depends on OptFrame C++ project, but it will (hopefully) be 
built automatically for Python users.

Installing with pip
-------------------

Installing `optframe` package in Python is quite easy with pip.

.. code-block:: shell

   python -m pip install optframe

.. warning::
    The standard configuration will require a modern c++ compiler with C++17 support, or maybe C++20.
    Note that, by 2022, this is already standard on recent MacOS software and Ubuntu 22.04 (g++ v11 is recommended... g++ v9 will not work!).
    On Windows/WSL environment, it is possible to upgrade WSL and g++. 
    Native Windows C++ compiler has not been tested yet... please try WSL first.


And that's it! You can skip to `Quick Start <./quickstart.html>`_ now.


Cloning from GitHub
-------------------

If you want to contribute to the project (or both), 
you may want to also download OptFrame C++ and make a symbolic link under `src` folder.

To clone OptFrame repository from GitHub and make symbolic link:

.. code-block:: shell

   git clone https://github.com/optframe/pyoptframe-dev.git
   git clone https://github.com/optframe/optframe.git
   ln -s  $(pwd)/optframe/include  pyoptframe/src/optframe-src


Then you can run basic tests with GCC or CLANG::

   cd pyoptframe
   make optframe_lib
   make demo_local

A `optframe_lib.so` file should be generated and demo should be run.

You can also change de OptFrame Python locally and test it::

   pip install .
   make test

After installing OptFrame Python (maybe using `pip`), user can start building
a solution to the problem at hand.


Welcome Message
---------------

A useful abstraction was introduced since OptFrame 4.1, called OptFrame Functional Core (FCore).
The idea of FCore is to provide a simplified access to OptFrame programming classes, by means
of closures and lambdas. This way, a project that typically had 8 to 10 files is reduced to a single
file (all included in headers!).

The first test on FCore is to see if it's correctly executing.
First, we need to instantiate a `optframe.Engine()` instance, then print its `welcome()` message:

..
    // THIS IS NOT PRINTED: COMMENT IN RESTRUCTURED TEXT (SEE REAL FILE INCLUSION BELOW)
    // file: 'mytest.py'
    import optframe

    engine = optframe.Engine()
    engine.welcome()

:code:`File 'mytest.py' located in 'demo/01_QuickstartWelcome/'`

.. literalinclude:: ../../demo/01_QuickstartWelcome/mytest.py
    :linenos:
    :language: python

Execute it on terminal
^^^^^^^^^^^^^^^^^^^^^^

One way to execute it on terminal is to follow these commands::

    python -m pip install optframe
    python mytest.py
    # Welcome to OptFrame Functional Core (FCore) - version 5.0-dev

A deeper explanation of OptFrame theoretical foundations can be found on `Concepts <./concepts.html>`_
section, so we will move fast here!

And that's it! You can skip to `Quick Start <./quickstart.html>`_ now.