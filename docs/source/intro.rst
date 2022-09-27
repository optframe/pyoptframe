Introduction
=============

.. hint::
    This is OptFrame Python project, so for OptFrame C++ please 
    see `OptFrame on GitHub <https://github.com/optframe/optframe>`_


OptFrame is a framework for modeling and solving challenging optimization 
problems via (meta)-heuristic techniques.
It is developed in modern C++ and ported to Python, aiming to provide both high computational 
efficiency and easy of use.
The project has started in 2008 at `Universidade Federal de Ouro Preto 
(UFOP) <https://www.ufop.br>`_ and considerably improved since then. Several master 
and PhD thesis have been developed on it, mostly at the Computing Institute 
of `Universidade Federal Fluminense (UFF) <http://www.ic.uff.br>`_. Its latest version 
v5 has been under development in 2022, with the introduction of several functional 
programming features and C++11/14/17/20 capabilities.

OptFrame supports several state-of-the-art `metaheuristics 
<https://en.wikipedia.org/wiki/Metaheuristic>`_, such as:

- `Genetic Algorithm <https://en.wikipedia.org/wiki/Genetic_algorithm>`_ and Evolution Strategies
- `Greedy Randomized Adaptive Search Procedures <https://en.wikipedia.org/wiki/Greedy_randomized_adaptive_search_procedure>`_ (GRASP)
- `Iterated Local Search <https://en.wikipedia.org/wiki/Iterated_local_search>`_ (ILS)
- `Simulated Annealing <https://en.wikipedia.org/wiki/Simulated_annealing>`_
- `Tabu Search <https://en.wikipedia.org/wiki/Tabu_search>`_
- `Variable Neighborhood Search <https://en.wikipedia.org/wiki/Variable_neighborhood_search>`_ (VNS)

And also `multi-objective optimization <https://en.wikipedia.org/wiki/Multi-objective_optimization>`_ 
metaheuristics, such as NSGA-II.

.. hint::
    
    The theoretical background behind OptFrame modeling is better described on OptFrame C++, please 
    see `OptFrame C++ Concepts on ReadTheDocs <https://optframe.readthedocs.io/en/latest/concepts.html>`_

.. hint::
    
    OptFrame C++ heavily uses templates, but manages to support this Python project 
    by means of the abstraction `OptFrame C++ Functional Core <https://optframe.readthedocs.io/en/latest/fcore.html>`_


If you have already :doc:`installed <../install>` OptFrame, you can jump to
:doc:`quick start <../quickstart>` to see how it works on practice.

Acknowledgements
-----------------

.. role::  raw-html(raw)
    :format: html

OptFrame has been developed with :raw-html:`&hearts;`, thanks to many contributors and
advices from brillant minds from academia.
Several researchers worldwide have contributed with ideas that represent the core of
OptFrame, specially: 

- Marcone Jamilson Freitas Souza *(for metaheuristic teaching and support)*
- Nenad Mladenovic *(for great works on neighborhood exploration)*
- Luiz Satoru Ochi *(for metaheuristic teaching and support)*
- Thibaut Lust *(for great ideas on multi-objective optimization)*
- El-Ghazali Talbi *(for great books on metaheuristics and optimization)*

Contributors
------------

Several contributors made this possible, please refer to the CONTRIBUTORS file on 
OptFrame C++ project on `GitHub <https://github.com/optframe/optframe>`_.

This project is currently maintained by `Igor M. Coelho <https://github.com/igormcoelho>`_.

License
-------

Project is free, and source code is dual licensed under LGPLv3 copyleft license and permissive MIT license.

Some side projects such as Scanner++ are released under MIT License.

See complete :doc:`license <../license>`.
