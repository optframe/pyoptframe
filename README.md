# pyoptframe
Python bindings for OptFrame Functional Core

[OptFrame](https://github.com/optframe/optframe) is a C++ framework for optimization problems, including techniques such as classic metaheuristics Simulated Annealing, Genetic Algorithm, 
Variable Neighborhood Search, Iterated Local Search, Tabu Search, Particle Swarm Optimization, NSGA-II, and other single and multi-objective methods.
This is a 10-year project with several practical applications in industry and academia, so feel free to use it.

## How to test

`make install` or `pip install .`

`make test`

## C++ Standard

We love Concepts and Optionals, so we require `C++20` as default. 
However, it is possible to adapt `setup.py` in order to allow for `C++17` with `-fconcepts` on GCC. 
If necessary (only C++17 is available), add this line on `setup.py`:

```
extra_compile_args=['--std=c++17', '-fconcepts']
```

## Example with 0-1 Knapsack Problem

Please see file `tests/test_engine_kp.py` for an example with 0-1 Knapsack Problem.

## Known Issues

All known issues fixed :)

## License

MIT License - 2022

