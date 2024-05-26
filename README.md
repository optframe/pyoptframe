# pyoptframe-dev

[![Documentation Status](https://readthedocs.org/projects/optframe/badge/?version=latest)](https://pyoptframe.readthedocs.io/en/latest/?badge=latest)

Development repo for draft versions of Python bindings for OptFrame Functional Core C++.


Install: `python -m pip install optframe`

Version: `pyoptframe v5.1.0`

Play on Jupyter Notebook: [BRKGA Traveling Salesman Problem Example](demo/OptFrame_BRKGA_Official.ipynb)

Documentation and Tutorials: see [PyOptFrame Quickstart](https://pyoptframe.readthedocs.io/en/latest/quickstart.html)

Beware that, after officially launched, this project may be migrated into [Official Optframe C++](https://github.com/optframe/optframe) repo (and same strategy applies to other future external language bindings).

### About OptFrame C++

[OptFrame](https://github.com/optframe/optframe) is a C++ framework for optimization problems, including techniques such as classic metaheuristics Simulated Annealing, Genetic Algorithm, 
Variable Neighborhood Search, Iterated Local Search, Tabu Search, Particle Swarm Optimization, NSGA-II, and other single and multi-objective methods.
This is a 10+ year project with several practical applications in industry and academia, so feel free to use it.

## For Developers

If you want to help, please see instructions on [Development.md](./Development.md).


### Advice for online environments

OptFrame now supports both `c++17` and `c++20`.

Before installing optframe online (such as google colab), check C++ compiler (typically GCC) version:

`x86_64-linux-gnu-gcc -v`

At least gcc-10 is required for C++20... if not enough, try to install g++-10 and make it default.
*Considering Jupyter notebook syntax*:
```
!apt install -y g++-10
!g++-10 --version
!update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 10
!update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 10
!update-alternatives --install /usr/bin/x86_64-linux-gnu-gcc gcc /usr/bin/gcc-10 10
```

## Tutorials

### Demos

Documentation and Tutorials: see [PyOptFrame Quickstart](https://pyoptframe.readthedocs.io/en/latest/quickstart.html)

Please see the demos on demo/ folder.

We also include some jupyter notebooks for playing.


### Example with 0-1 Knapsack Problem (tests)

Also see file `tests/test_engine_kp.py` for an example with 0-1 Knapsack Problem,
used on internal tests.

### More tutorials

Please read the official tutorials for OptFrame C++, 
as they may give ideas for python too: https://optframe.readthedocs.io/

Also see the Examples and demo folders on C++ project: [github.com/optframe/optframe](https://github.com/optframe/optframe).


## Technical discussions and Roadmap
### C++ Standard and Compiler Support

We love Concepts and Optionals, so we require `C++20` as default. 
However, it is possible to adapt `setup.py` in order to allow for `C++17` with `-fconcepts` on GCC. 
If necessary (only C++17 is available), add this line on `setup.py`:

```
extra_compile_args=['--std=c++17', '-fconcepts']
```

For the moment, GCC and CLANG are officially supported, but more compilers can be added to the list, if demand exists.


### `optframe_lib` API Organization

The API on `optframe_lib` is organized in distict **API levels**.

Every function on `optframe_lib` API starts with the prefix `optframe_apiXy`, where
`X` represents the level and `y` represents the main evaluation type considered.
For now, we support `X=1` and `y=d`, meaning that API is meant for `float64` (or `double`) evaluation
spaces (but we certainly plan to add support for `i32`, `i64` and other types).

Regarding the API level strategy:

- level 0: only for raw (an unsecure) access to internal OptFrame functions
   * only use this for testing new features or making extremely efficient and direct function calls to OptFrame internals
- level 1 (STANDARD): this level must provide basic access to fundamental search techniques
and to all basic examples
- level 2 (ADVANCED): this level WILL (in the future) also include re-evaluation strategies and other more advanced features of OptFrame C++
- level 3+ (???): maybe we can use this to split advanced functionalities from API2, but only future can tell

In the future, we can also use greater API number to implement possible compatibility breaking features... only future will tell.

### Versioning Strategy

Versioning should follow OptFrame C++ project on MAJOR and MINOR, leaving PATCH field to be different, if necessary. Examples: 

- v 5 dot 1 dot 3 should include OptFrame C++ 5 dot 1.
- v 5 dot 4 dot 5 could include OptFrame C++ 5 dot 4 dot 8 OR 5 dot 4 dot 1, but NOT 5 dot 6 dot x.

## Known Issues

All known issues fixed :)

## Thanks

Thanks to the general help from Internet posts, this project could be packaged on Python (there are many links all around the source code mentioning the respective authors).

Also thanks for the encouragement and fruitful discussions with my students, specially, Rafael Albuquerque, Marcos Souza, Victor Silva and Fellipe Pessanha.

## License

At your choice:

- [LICENSE-MIT](./LICENSE-MIT.txt)
- [LICENSE-LGPLv3+](./LICENSE-LGPL-3.0-or-later.txt)

Copyleft 2023

Igor Machado Coelho

