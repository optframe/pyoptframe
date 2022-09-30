Quick start
=============


OptFrame Python is built upon OptFrame C++, a framework focused in solving challenging optimization problems, specially by means
of metaheuristic techniques.
This package abstracts away the C++ complexity and makes it easier for users to model efficient
optimization techniques directly on Python.

After `installing <./install.html>`_ OptFrame Python (maybe using `pip`), user can start building
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

.. hint::
    The examples from OptFrame Python project follow the same idea from OptFrame C++. 
    Understanding both can be interesting to gain more confidence on the framework.
    If feeling brave, take a look at `OptFrame C++ on ReadTheDocs <https://optframe.readthedocs.io/en/latest/quickstart.html>`_


First Example: 0-1 Knapsack Problem and Simulated Annealing
-----------------------------------------------------------

Let's consider a classic problem: the 0-1 Knapsack Problem (KP).

|knapsack|
By: Dake `CC BY-SA 2.5 <https://commons.wikimedia.org/wiki/File:Knapsack.svg>`_

.. |knapsack| image:: _figs/Knapsack.svg
   :width: 300
   :alt: A knapsack and some items (from wikipedia)

Given a set of items :math:`I`, the KP consists in selecting some items :math:`S \subseteq I`,
such that the sum of weights :math:`w_i` (for each selected item) do not exceed knapsack
capacity :math:`Q`, and profit :math:`p_i` of the selected items is maximized.

$$maximize\\; \\sum_{i \\in S} p_i$$
$$\\sum_{i \\in S} w_i \\leq Q$$
$$S \\subseteq I$$

Solution and Evaluation Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. role:: pythoncode(code)
  :language: python


Users must first define a *Representation*, which is a data structure that represents
an element in the *Solution Space* for the KP. A natural candidate here is a *list of booleans*, 
since we need to decide if we are going to carry each item or not. In Python, an interesting
approach is to use native list or even advanced containers of :pythoncode:`numpy` for greater performance.

User also needs to specify the data type for the *Objective Space*, in general a numeric type.
The standard API of OptFrame Python adopts `float64` or `double` type, and this API is called `API1d`.

.. hint::
    There are more advanced APIs, other than `API1d`, which we will explore in the future.

We declare a `XSolution <./concepts.html>`_ class implemented as 
`SolutionKP`. 
Note that XSolution concept requires solution to be printable (through :pythoncode:`__str__` method) 
and fully copiable (through :pythoncode:`__deepcopy__` method):

.. 
    // COMMENTS!!!
    class SolutionKP(object):
    ...

.. literalinclude:: ../../demo/02_QuickstartKP_SA/KP-fcore-ex-part1.py
    :linenos:
    :language: python


.. hint::
    For more advanced APIs, we will need a XESolution pair, containing the solution
    and evaluation value. In the future we will see more of this.


Problem Context
^^^^^^^^^^^^^^^

Users will need to store general problem information (such as profits and weights of items),
so a *ProblemContextKP* can be introduced.


.. 
    // COMMENTS
    // ...
    class ProblemContextKP:
        ...

.. literalinclude:: ../../demo/02_QuickstartKP_SA/KP-fcore-ex-part2.py
    :linenos:
    :language: python

.. hint::
    ProblemContext is a user-defined class that can have any desired format. A 'load' function
    is just a suggestion, but not at all necessary. An OptFrame `engine` is also suggested to
    be stored here, since this problem will be available to all components.

Random Constructive
^^^^^^^^^^^^^^^^^^^

We need to have some initial solution for the search process, so we just proceed in a random manner.
For simplicity, we allow infeasible solutions to be generated (as if capacity was infinite).
Any function name is acceptable (such as `mycallback_constructive`), but pay attention to the 
function parameters (receives problem and returns solution):

..
    // COMMENTS
    def mycallback_constructive(problemCtx: ProblemContextKP) -> SolutionKP:
    ...

.. literalinclude:: ../../demo/02_QuickstartKP_SA/KP-fcore-ex-part3.py
    :linenos:
    :language: python

.. hint::
    User can also define many advanced constructive techniques in a similar manner, such as greedy 
    and greedy randomized approaches.


Evaluator
^^^^^^^^^

Now it's time to define an evaluation (or objective) function. According to the goal of 
maximizing the profits, we iterate over selected items to accumulate profit and weights.
As discussed in constructive section, we allow accumulated weight to surpass knapsack capacity,
for infeasible configurations. 
To discourage that, we introduce negative penalization whenever capacity is exceeded (assuming weight -1000000):

..
    // COMMENTS
    def mycallback_fevaluate(pKP: ProblemContextKP, sol: SolutionKP):
    ...

.. literalinclude:: ../../demo/02_QuickstartKP_SA/KP-fcore-ex-part4.py
    :linenos:
    :language: python

We have defined :code:`mycallback_fevaluate` function, 
and later we will define its optimization direction ( in this case, `maximization`).


.. hint::
    User can also choose to :code:`MINIMIZE` if dealing with a minimization problem. For multi-objective
    problems and Pareto optimization, user should visit `Multi-Objective <./advanced.html#multi-objective>`_ section.


Neighborhood Structure
^^^^^^^^^^^^^^^^^^^^^^

In order to improve a given solution, several metaheuristics employ `Local Search Optimization <https://en.wikipedia.org/wiki/Local_search_(optimization)>`_
techniques based on the concept of Neighborhood Structure. 
Every neighborhood is related to a move operator, which is required (on FCore) to have an undo operation (capable of reverting the effects of the move).


We create a :code:`BitFlip` move, that changes the :code:`true/false` selection of a given item :math:`k`.
In this case, the `move structure` (representation of the move) is just an :code:`int`, that represents the flipped item.

.. 
    // COMMENTS
    MoveBitFlip ...

Note the three static methods `apply`, `canBeApplied` and `equals`.

.. literalinclude:: ../../demo/02_QuickstartKP_SA/KP-fcore-ex-part5.py
    :linenos:
    :language: python

Now, it's time to define a neighborhood generator for the move.
OptFrame has three main types of neighborhoods: :code:`NS`, :code:`NSSeq` and :code:`NSEnum`.

In this example, we will use :code:`NS`, since it only requires the generation of random moves:

..
    // COMMENTS
    random ...

.. literalinclude:: ../../demo/02_QuickstartKP_SA/KP-fcore-ex-part6.py
    :linenos:
    :language: python

.. hint::
    It is usually a good idea to start developing over the simplest neighborhood, which is :code:`NS`.
    Most (non-deterministic) metaheuristics only requires a :code:`NS`, as it only requires the generation of random moves.
    More advanced neighborhoods based on iterators, such as :code:`NSSeq` and :code:`NSEnum` are only required for advanced `Local Search <./advanced.html#local-search>`_ methods.


Time to Test!
^^^^^^^^^^^^^

At this point, you can already test many nice metaheuristics and solve your knapsack problem!
We use the following code to load a problem instance (see `Complete Example`_ after):

.. 
    // COMMENTS!!
    random.seed(10) ....

.. literalinclude:: ../../demo/02_QuickstartKP_SA/mainKP-fcore-ex-part2.py
    :linenos:
    :language: python

.. hint::
    It is useful to test every FCore structure independently, so as to develop unit testing for them.

Now we register evaluation and constructive into the engine.
Then we test the constructive and evaluator:

..
    // COMMENTS
    ...

.. literalinclude:: ../../demo/02_QuickstartKP_SA/mainKP-fcore-ex-part3.py
    :linenos:
    :language: python

Now we give an example with of the most well-known metaheuristics: the `Simulated Annealing <https://en.wikipedia.org/wiki/Simulated_annealing>`_.
It has few parameters, including: initial temperature :code:`T0`, cooling factor :code:`alpha`, and iterations per temperature :code:`iterT`.

.. hint::
    Note that we will use OptFrame Component Builder syntax, 
    to automatically generate a native C++ Component based on a build string.
    For more details, see the (TODO) Component Builder list on OptFrame C++ ReadTheDocs (TODO).

.. 
    // COMMENTS
    SAnnealing...
    
.. literalinclude:: ../../demo/02_QuickstartKP_SA/mainKP-fcore-ex-part4.py
    :linenos:
    :language: python

Complete Example
----------------

.. warning::
    We present a complete example below. Note that some small differences may exist due to updates in tutorial, including language details.
    Feel free to check OptFrame C++ folder :code:`OptFrame/Examples` for other examples on FCore and OptFrame Classic.

Example is divided in two files: :code:`KP-fcore-ex.py` and :code:`mainKP-fcore-ex.py`.
The file :code:`mainKP-fcore-ex.py` aggregates all components for execution.

.. hint::
    This example could be made in a single file, to be even simpler. However, we recommend users to have  
    a clear separation for the header declaration of *FCore components* (on :code:`KP-fcore-ex.py`) 
    from the :code:`main()` entrypoint (on :code:`mainKP-fcore-ex.py`), since unit testing is much simpler when these are decoupled.


*mainKP-fcore-ex.py*

:code:`File 'mainKP-fcore-ex.py' located in 'demo/02_QuickstartKP_SA/'`

.. literalinclude:: ../../demo/02_QuickstartKP_SA/mainKP-fcore-ex.py
    :linenos:
    :language: python

*knapsack-example.txt*

:code:`File 'knapsack-example.txt' located in 'demo/02_QuickstartKP_SA/'`

.. literalinclude:: ../../demo/02_QuickstartKP_SA/knapsack-example.txt
    :linenos:
    :language: c++

To run it::

    python3 mainKP-fcore-ex.py
