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
    The standard configuration will require a modern c++ compiler with C++20 support.
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


And that's it! You can skip to `Quick Start <./quickstart.html>`_ now.