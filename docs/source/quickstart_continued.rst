Quick start (Continued)
=======================

We expand the knowledge from `Quick Start <./quickstart.html>`_ where the user
has learned how to `Install <./install.html>`_ OptFrame, and how to compile and
test a `Simulated Annealing <https://en.wikipedia.org/wiki/Simulated_annealing>`_ metaheuristic
for the classic 0-1 Knapsack Problem (01KP).

We demonstrate how to update this code for other metaheuristics, for the classic Traveling Salesman Problem (TSP).

Second example: Traveling Salesman Problem, Local Search and Random Keys Genetic Algorithm
------------------------------------------------------------------------------------------

At this point, we assume the reader is familiarized with the Traveling Salesman Problem...
we intend to expand this section in the future with figures and more motivation (for now, sorry, and let's move on).

TSP Solution definition
^^^^^^^^^^^^^^^^^^^^^^^

We define a TSP solution as a permutations of $N$ cities being visited by a Traveling Salesman.
In this representation, each city is represented as a number $0..N-1$, being a solution a
vector of N integers (example: [0,2,3,1] means that solution starts from city 0, then follows to city 2,
then city 3, then city 1, and finally comes back to city 0). 
Objective is to find a route that minimizes distance between the $N$ visited cities.

We may define SolutionTSP and its objective value (`double` by default on `API1d`, or `int` on `API1i32`).

..
    // COMMENTS 
    ... SolutionTSP...

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part1.py
    :linenos:
    :language: python


Problem Data
^^^^^^^^^^^^

We read a matrix of distances between pairs of cities (considering Euclidean distance), and
store in a structure named ProblemContextTSP. Note that we round the result to int, just to allow
precise value calculation (but one may use float or double, and then manage the floating-point errors).
Other option would be to adopt a strict int `API1i32`.

..
    // COMMENTS
    ... ProblemContextTSP ..

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part2.py
    :linenos:
    :language: python

Finally, we created a function `load()` to manage de input of data.


Evaluation
^^^^^^^^^^^

Objective calculation can be done by using an evaluator callback, which is 
compatible to OptFrame Core Evaluator (for single objectives) and 
GeneralEvaluator (for single and multiple objectives).

..
    // COMMENTS
    ... evaluate

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part3.py
    :linenos:
    :language: python


Search methods based on neighborhoods
-------------------------------------

The next components will depend on the type of search method used, we start with 
neighborhood-based search techniques.

Random constructive
^^^^^^^^^^^^^^^^^^^

In a similar manner with Knapsack example (on Quickstart part 1), we define
a random solution generator.

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part4.py
    :linenos:
    :language: python

First move operator: Swap
^^^^^^^^^^^^^^^^^^^^^^^^^

We start with a Move operator capable of exchanging two elements from a given TSP solution.

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part5.py
    :linenos:
    :language: python

We have four types of neighborhood definitions in OptFrame (NS, NSFind, NSSeq and NSEnum), but
two major are NS and NSSeq.

NS works well for random neighborhoods, with no intent of explicitly
visiting all possible neighbors (also useful for continuous or infinite neighborhoods).
Swap move and NS definition can be seen below.


.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part6.py
    :linenos:
    :language: python

We now define the NSSeq neighborhood with a explicit iterator definition, that requires four
operations: first (initializes first valid move), next (skips to next valid move), 
current (returns current move) and isDone (indicates if no move exists).

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/TSP-fcore-part7.py
    :linenos:
    :language: python

.. hint::
    According to groundbreaking ideas from Variable Neighborhood Search community, the user 
    should create multiple neighborhoods, with different ideas in each one, in order to better
    explore the solution space.


Complete Example for TSP Components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For simplicity, we separate the main TSP components in a file named :code:`TSP-fcore.py`.

.. hint::
    This example could be made in a multiple files as a package, for the separation 
    of *FCore components* (on :code:`TSP-fcore.py`) and the :code:`main()` entrypoint depending on method used.
    However, we just merge them into a single file on each application, for simplicity, e.g., :code:`mainTSP-fcore-ils.py` or :code:`mainTSP-fcore-brkga.py`.

*TSP-fcore.py*

:code:`File 'TSP-fcore.py' located in 'demo/03_QuickstartTSP_VNS_BRKGA/'`

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/TSP-fcore.py
    :linenos:
    :language: python


Exploring with neighborhood exploration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OptFrame supports several strategies for neighborhood exploration, such as:
First Improvement, Best Improvement, Random Selection and Multi Improvement.
We can also combine several local search strategies in a multiple strategy
called Variable Neighborhood Descent (VND).

.. hint::
    Note that we will use OptFrame Component Builder syntax, 
    to automatically generate a native C++ Component based on a build string.
    For more details, see the (TODO) Component Builder list on OptFrame C++ ReadTheDocs (TODO).


:code:`File 'mainTSP-fcore-ils-part2.py' located in 'demo/03_QuickstartTSP_VNS_BRKGA/'`

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/mainTSP-fcore-ils-part2.py
    :linenos:
    :language: python

If one wants to build a complete metaheuristic, the Iterated Local Search (ILS) or a Variable
Neighborhood Search (VNS).
The ILS is based on general perturbation concept, so we will use the concept of Levels of 
Perturbation, that are increased when stuck in a poor quality local optimum. We adopt a perturbation 
strategy that tries to escape at level p by applying p+2 random moves, e.g., at level 0,
2 random moves are applied, and so on.

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/mainTSP-fcore-ils-part3.py
    :linenos:
    :language: python




Complete Example for ILS
^^^^^^^^^^^^^^^^^^^^^^^^

We provide the main file for TSP ILS :code:`mainTSP-fcore-ils.py`.

*mainTSP-fcore-ils.py*

:code:`File 'mainTSP-fcore-ils.py' located in 'demo/03_QuickstartTSP_VNS_BRKGA/'`

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/mainTSP-fcore-ils.py
    :linenos:
    :language: python

To run it::

    python3 mainTSP-fcore-ils.py 


Search methods based on random keys
-----------------------------------


We finish with the Biased Random Key Genetic Algorithm (BRKGA), a simple metaheuristic
inspired by classic Genetic Algorithm, using the solution representation of $n$ Random Keys, 
which are $[0,1]^n$ float values.

Random key generation
^^^^^^^^^^^^^^^^^^^^^

The BRKGA requires an initial solution generator, which is in this case, $n$ random [0,1] floats.
This can be done automatically by the method (since its trivial do generate $n$ [0,1] random numbers),
but we choose to demonstrate manually (by inheriting from OptFrame Core class Initial Population).

This is good to tune the degree of randomness (number of random digits) and also the random function used.

..
    // COMMENTS
     MyRandomKeysInitPop

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/mainTSP-fcore-brkga-part2.py
    :linenos:
    :language: python

BRKGA decoding
^^^^^^^^^^^^^^^

BRKGA also requires a decoder function, that maps this array of random keys into a permutation.

This can be easily done with Functional Core class FDecodeRK, and an interesting approach based
on sorting the keys, related to a predefined indexing of each key.

..
    // COMMENTS
    pair<Evaluation<double>, vector<int>>
    fDecode(const vector<double>& rk)
    {
        vector<pair<double, int>> v(rk.size());
        int k = 0;
        for (unsigned i = 0; i < v.size(); i++)
            v[k] = pair<double, int>(rk[i], i);

        // sort the pairs according to the random key value 
        sort(v.begin(), v.end(), [](const pair<double, int>& i, const pair<double, int>& j) -> bool {
            return i.first < j.first;
        });

        // TSP representation is vector<int>
        vector<int> p(v.size());
        for (unsigned i = 0; i < v.size(); i++)
            p[i] = v[i].second;

        Evaluation<double> e = ev.evaluate(p);
        return make_pair(e, p);
    }

    // evaluator random keys (for TSP)
    FDecoderRK<std::vector<int>, Evaluation<>, double, MinOrMax::MINIMIZE> decoder{
        fDecode 
    };


.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/mainTSP-fcore-brkga-part3.cpp
    :linenos:
    :language: c++

BRKGA with TSP
^^^^^^^^^^^^^^^

We are ready to build a TSP instance with 3 cities with coordinates (10,10), (20,20) and (30,30),
and invoke a BRKGA to solve it.

The parameters of BRKGA are: decoding function, initial solution generator, population size, number of iterations,
also rates for mutation (randomness), elite (best solutions), preference for elite solutions, and finally, a random generation method.

..
   // COMMENTS
   sref<RandGen> rg = new RandGen;

   // load data into problem context 'pTSP'
   Scanner scanner{ "3\n1 10 10\n2 20 20\n3 30 30\n" };
   pTSP.load(scanner);
   std::cout << pTSP.dist << std::endl;

   sref<DecoderRandomKeys<ESolutionTSP::first_type, ESolutionTSP::second_type, double>> _decoder = decoder;
   sref<InitialPopulation<std::pair<vector<double>, ESolutionTSP::second_type>>> _initPop = new MyRandomKeysInitPop(pTSP.n); // passing key_size

   //eprk, pTSP.n, 1000, 30, 0.4, 0.3, 0.6
   BRKGA<ESolutionTSP, double> brkga(
     _decoder,
     MyRandomKeysInitPop(pTSP.n, rg), // key_size = pTSP.n
     30,
     1000,
     0.4,
     0.3,
     0.6,
     rg);

   auto searchOut = brkga.search(10.0); // 10.0 seconds max

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/mainTSP-fcore-brkga-part4.cpp
    :linenos:
    :language: c++

The result from searchOut can be split in two parts, an error code and the returned solution 
(the same as in Simulated Annealing or any other OptFrame search method).


Complete Example for BRKGA
^^^^^^^^^^^^^^^^^^^^^^^^^^

We provide the main file for TSP BRKGA :code:`mainTSP-fcore-brkga.cpp`.

*mainTSP-fcore-brkga.cpp*

:code:`File 'mainTSP-fcore-brkga.cpp' located in 'demo/03_QuickstartTSP_VNS_BRKGA/'`

.. literalinclude:: ../../demo/03_QuickstartTSP_VNS_BRKGA/mainTSP-fcore-brkga.cpp
    :linenos:
    :language: c++

More Examples 
-------------

For a other examples, see folder Examples/FCore-BRKGA and execute :code:`bazel build ...`

.. warning::
    Feel free to check folder :code:`OptFrame/Examples` for other examples on FCore and OptFrame Classic.

