# pyoptframe
Python bindings for OptFrame Functional Core

[OptFrame](https://github.com/optframe/optframe) is a C++ framework for optimization problems, including techniques such as classic metaheuristics Simulated Annealing, Genetic Algorithm, 
Variable Neighborhood Search, Iterated Local Search, Tabu Search, Particle Swarm Optimization, NSGA-II, and other single and multi-objective methods.
This is a 10-year project with several practical applications in industry and academia, so feel free to use it.

## How to test

`make install` or `pip install .`

`make test`

## C++ Standard and Compiler Support

We love Concepts and Optionals, so we require `C++20` as default. 
However, it is possible to adapt `setup.py` in order to allow for `C++17` with `-fconcepts` on GCC. 
If necessary (only C++17 is available), add this line on `setup.py`:

```
extra_compile_args=['--std=c++17', '-fconcepts']
```

For the moment, GCC and CLANG are officially supported, but more compilers can be added to the list, if demand exists.

## Tutorials

Please read the official tutorials for OptFrame C++: https://optframe.readthedocs.io/

Tutorials specific for OptFrame Python is coming!

## Example with 0-1 Knapsack Problem

Please see file `tests/test_engine_kp.py` for an example with 0-1 Knapsack Problem.

## `optframe_lib` API Organization

The API on `optframe_lib` is organized in distict **API levels**.

Every function on `optframe_lib` API starts with the prefix `optframe_apiXy`, where
`X` represents the level and `y` represents the main evaluation type considered.
For now, we adopt `y=d`, meaning that API is meant for `float32` (or `double`) evaluation
spaces (but we certainly plan to add support for `i32`, `i64` and other types).

Regarding the API level strategy:

- level 0: only for raw (an unsecure) access to internal OptFrame functions
   * only use this for testing new features or making extremely efficient and direct function calls to OptFrame internals
- level 1 (STANDARD): this level must provide basic access to fundamental search techniques
and to all basic examples
- level 2 (ADVANCED): this level WILL (in the future) also include re-evaluation strategies and other more advanced features of OptFrame C++
- level 3+ (???): maybe we can use this to split advanced functionalities from API2, but only future can tell

In the future, we can also use greater API number to implement possible compatibility breaking features... only future will tell.

## Known Issues

All known issues fixed :)

## Thanks

Thanks to the general help from Internet posts, this project could be packaged on Python (there are many links all around the source code mentioning the respective authors).

Also thanks for the encouragement and fruitful discussions with my students, specially, Rafael Albuquerque, Marcos Souza, Victor Silva and Fellipe Pessanha.

## License

MIT License || LGPLv3 License  (at your choice)

Copyleft 2022

Igor Machado Coelho

