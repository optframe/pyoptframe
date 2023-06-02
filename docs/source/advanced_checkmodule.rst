Advanced CheckModule and Debugging
==================================

Some advanced tricks and optimization techniques.

.. danger::
    This section is incomplete!


Introducing Check Module
^^^^^^^^^^^^^^^^^^^^^^^^

Check Module allows users to test classic model components for an specific problem,
such as: XSolution, Constructive, Evaluator, NS, NSSeq and Move.
This is specially useful for moves, where apply and undo logic typically cause problems.
The idea is to run check module with increasingly larger number of parameters (starting from 100, 10),
that will take longer to complete, but will better explore random component configurations that
could cause runtime issues.

From the 0-1 knasack demo, we have:

.. code-block:: python

    pKP.engine.check(100, 10, False)

This will invoke check module with `verbose=False` and `(iter1,iter2)=(100,10)`.

Debugging
^^^^^^^^^

Problems typically occur during check module (this is better than having an unexpected runtime issue!).
To debug, it is interesting to properly configure verbosity level on components and the optframe engine.

.. code-block:: python

    # make component debug level (loglevel 4)
    # MUST USE THIS BEFORE BUILDING THE COMPONENT, NOT AFTER!
    pKP.engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "4")

Other verbosity flags can be used as the optframe engine log level:

.. code-block:: python

    # make engine silent (loglevel 0)
    pKP.engine.experimental_set_parameter("ENGINE_LOG_LEVEL", "0")

Between Silent (level 0) and Debug (level 4), there are other alternatives, try to explore them.

Remember to always flush your debug messages on python, otherwise they may be lost after some execution error!

.. code-block:: python

    # remember to flush python messages during debug
    print("this is a debug message for component: ", component, flush=True)

Using Retry Debug on Check Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A useful trick on debugging with check module is to use Retry Debug feature.
When enabled, this feature allows CheckCommand to repeat some previously failed test,
while allowing user to change Engine into some verbose mode, useful for debugging.
This behavior is enabled by default, but user can also personalize the onFail callaback:

.. code-block:: python

    # declare some personalized onfail callback, that makes Component Log Level be set to Debug
    def my_personalized_onfail(code: CheckCommandFailCode, engine : Engine) -> bool:
        engine.experimental_set_parameter("COMPONENT_LOG_LEVEL", "4")
        print("MY ON FAIL! code:", CheckCommandFailCode(code), "cll:", engine.component_loglevel, flush=True)
        return False

On MAIN pass this callback to check (according to knapsack example):

.. code-block:: python

    # use personalized callback
    pKP.engine.check(100, 10, False, my_personalized_onfail)
    # or just use default one, by avoiding last parameter...
    # pKP.engine.check(100, 10, False)

Finally, we can cause some error in MoveBitFlip knapsack example, and take advantage of the debug flag:

.. code-block:: python

    class MoveBitFlip(object):
        def __init__(self, _k :int):
            self.k = _k
        def __str__(self):
            return "MoveBitFlip("+str(self.k)+")"
        @staticmethod
        def apply(pKP: ExampleKP, m: 'MoveBitFlip', sol: ExampleSol) -> 'MoveBitFlip':
            if pKP.engine.component_loglevel == LogLevel.Debug:
                print("DEBUG: apply move: ", m, flush=True)
            sol.bag[m.k] = 1 - sol.bag[m.k]
            rev = MoveBitFlip(m.k + 1) # <----- THIS +1 IS A BUG !!!
            if pKP.engine.component_loglevel == LogLevel.Debug:
                print("DEBUG: reverse move is: ", rev, flush=True)
            return rev
        @staticmethod
        def canBeApplied(problemCtx: ExampleKP, m: 'MoveBitFlip', sol: ExampleSol) -> bool:
            return True
        @staticmethod
        def eq(problemCtx: ExampleKP, m1: 'MoveBitFlip', m2: 'MoveBitFlip') -> bool:
            return m1.k == m2.k

In this case, user can expect some message of this kind:

    CheckCommand: ON FAIL! code: CheckCommandFailCode.CMERR_MOVE_EQUALS  cll: LogLevel.Info  set to Debug.
    DEBUG: apply move:  MoveBitFlip(3)
    DEBUG: reverse move is:  MoveBitFlip(4)


Using specific configurations and Builders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OptFrame has a Component Builder syntax to instantiate some component. 
For example, to build Simulated Annealing, we can do that with beautiful Python wrapper as in KP example:

.. code-block:: python

    # build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
    sa = BasicSimulatedAnnealing(pKP.engine, 0, 0, list_idx, 0.98, 100, 99999)
    sout = sa.search(10.0)
    print("Best solution: ",   sout.best_s)
    print("Best evaluation: ", sout.best_e)

However, one may also build this metaheuristic manually using Component Builder syntax:

.. code-block:: python

    # build Simulated Annealing with alpha=0.98 T0=99999 and IterMax=100
    gs_idx = pKP.engine.build_global_search(
        "OptFrame:ComponentBuilder:GlobalSearch:SA:BasicSA",
        "OptFrame:GeneralEvaluator:Evaluator 0 OptFrame:InitialSearch 0  OptFrame:NS[] 0 0.98 100 99999")
    print("gs_idx=", gs_idx)

    # run Simulated Annealing for 10.0 seconds
    lout = pKP.engine.run_global_search(gs_idx, 10.0)
    print('lout=', lout)

The advantage of learning such syntax is to better explore OptFrame components and methods that are
not yet available on Python using wrappers.

Other important thing is to explore experimental configurations, such as `NS_VALID_RANDOM_MOVE_MAX_TRIES`:

.. code-block:: python

    print("==-Experimental-==")
    json_out = pKP.engine.experimental_get_parameter("")
    print("json_out=",json_out)
    # THIS SHOULD BE DONE BEFORE BUILDING A NS OBJECT
    pKP.engine.experimental_set_parameter("NS_VALID_RANDOM_MOVE_MAX_TRIES", "2")
    json_out = pKP.engine.experimental_get_parameter("")
    print("json_out=",json_out)

Parameter `NS_VALID_RANDOM_MOVE_MAX_TRIES` allows dealing with invalid moves, by 
trying multiple times before giving up. Many of these configurations are very
important, and are directly available over C++ project, being now ported to Python as
requested by users.

If you are missing some important OptFrame C++ feature on Python, please let us know!

