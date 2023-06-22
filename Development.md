# Development for optframe python

If you want to help or adjust the python/c++ optframe library, please follow these instructions.

## How to test locally (devs only)

First, you need to understand the structure of the project.
There are two ways to build the library locally:

1. Locally with submodule: using the optframe git submodule hosted at thirdparty folder
2. On package: that demands setuptools to automatically download a **tagged** optframe C++ version for local installation

When adjusting C++ optframe library locally with submodules, one may need to build it locally (with `make load_thirdparty` and `make optframe_lib`).
This allows changing and playing with C++ code (hosted on `thirdparty/optframe-external`), without the need to commit remote C++ changes or create some official C++ tag.

When changes are consolidated and tested, one may want to push these changes on OptFrame C++ project, and then create a tag. Push the C++ tag (diretly on OptFrame C++ project) and update [setup.py](setup.py) file on line:

```
        subprocess.check_call(
            ['git', 'clone', '--depth', '1', '--branch', '5.0.14', 'https://github.com/optframe/optframe', 'optframe-git'])
```

Then, it's possible to locally test the package (with `make clean` and `make install`), 
as it will download remote C++ project and build it locally with setuptools.

Sometimes, it's also useful to remove existing optframe package with: `pip uninstall optframe`

To do both things, just type `make test_local` and `make test_package`... or just `make test`!

## Old instructions

### With Local Package Manager

`make install` or `pip install .`

`make test`

### Without Package Manager (local only)

```
make optframe_lib
make demo_local
```

## Packaging instructions

Edit `setup.py`.

Edit `pyproject.toml`.

`virtualenv venv`

`source venv/bin/activate`

`python -m pip install pip-tools`

`pip-compile pyproject.toml`

`pip-sync`

For versioning:

`python3 -m pip install bumpver`

`bumpver init`

**To increase PATCH number:**

`bumpver update --patch`

Clean existing dist folder:

`rm -f dist/*`

Build and check:

`python3 -m pip install build twine`

`rm -f dist/* && python3 -m build`

`twine check dist/*`

Remove .whl to prevent error:

`rm -f dist/*.whl`

Update on test repository (not working fine for now):

`twine upload -r testpypi dist/* --verbose`

Test if OK on test package website:

`python3 -m pip install -i https://test.pypi.org/simple optframe --upgrade`

Finally, update to main repository:

`twine upload dist/*`

`python3 -m pip install optframe --upgrade`

Thanks again to: https://realpython.com/pypi-publish-python-package/

## License

This project is dual licensed on MIT and LGPLv3+. Please read LICENSE-* files.
