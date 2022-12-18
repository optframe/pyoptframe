# ===============
# https://github.com/himbeles/ctypes-example/blob/master/setup.py
# https://stackoverflow.com/questions/4529555/building-a-ctypes-based-c-library-with-distutils
# ===============

#
# STEP 1 - VERY GOOD DOCUMENTATION: https://setuptools.pypa.io/en/latest/userguide/ext_modules.html
#

from setuptools import setup, Extension
# from setuptools import find_packages # NO GOOD, YET...
import subprocess  # IMPORTANT FOR LOCAL GIT CLONE, OR 'ls -la'...
#  https://stackoverflow.com/questions/4529555/building-a-ctypes-based-c-library-with-distutils
from distutils.command.build_ext import build_ext as build_ext_orig
# Why?
import os

#
# trying this... https://stackoverflow.com/questions/59772476/how-to-write-setup-py-to-include-a-specific-git-repo-as-a-dependency
# this seems to require 'find_packages' and install_requires for remote git.... let's see!
# TOO BAD! Only seem to work for Python packages, not a remote C++ git repo... let's do manually then.
#

# WHY???
# from distutils import sysconfig


class CTypesExtension(Extension):
    pass


class MyBuildExt(build_ext_orig):
    # 'run' from: https://stackoverflow.com/questions/45599346/ask-setuptools-to-git-clone-c-repository
    def run(self):
        # ==== clone optframe from remote git repo ====
        # TODO: MUST FIND A BETTER WAY! NOT GOOD TO HAVE 'rm' COMMAND HERE!
        # fatal: destination path 'optframe-git' already exists and is not an empty directory.
        #
        # PLAN B
        # mkdir -p ...
        # git init
        # git remote add origin [my-repo]
        # git fetch
        # git checkout origin/master -ft
        subprocess.check_call(
            ['git', 'clone', '--depth', '1', '--branch', '5.0.7', 'https://github.com/optframe/optframe', 'optframe-git'])
        # ===== check that clone() was done fine ======
        # subprocess.check_call(
        #    ['ls', '-la', 'optframe-git'])
        build_ext_orig.run(self)

    def build_extension(self, ext):
        self._ctypes = isinstance(ext, CTypesExtension)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + '.so'
        return super().get_ext_filename(ext_name)


this_directory = os.path.abspath(os.path.dirname(__file__))
#
# ========== CHECK FILES ON CURRENT DIRECTORY (DEBUG) ========
#print("MY DIR: ", this_directory)
#subprocess.run(["ls", "-l", this_directory+"/src"])
# ============================================================

# WHY?????
# destination_path = sysconfig.get_python_lib()
# => /usr/lib/python3/dist-packages
# print("DEST PATH: ", destination_path)

setup(
    name="optframe",
    version="5.0.18rc0",
    py_modules=["optframe.engine"],
    ext_modules=[
        CTypesExtension(
            "optframe.optframe_lib",
            ["optframe/optframe_lib.cpp"],
            #
            # ========== ONLY IF LOCAL TESTING IS USED ===========
            # include_dirs=[os.path.join(
            #    this_directory, "./src/optframe-src/include")],
            #
            # ============ ONLY IF REMOTE GIT IS USED ============
            include_dirs=[os.path.join(
                this_directory, "./optframe-git/include")],
            #
            # ====================================================
            # TODO: we should start using c++20 ASAP...
            # Are Ubuntu / Windows / WSL2 users ready?
            #
            extra_compile_args=['--std=c++20']
            # IF ONLY C++17 IS SUPPORTED, ON GCC, USE THIS (WE NEED CONCEPTS):
            # extra_compile_args=['--std=c++17', '-fconcepts']
        ),
    ],
    # package_data includes data from 'src/' folder, by default
    package_data={
        # =========================================================
        #           THIS IS USEFUL FOR LOCAL TESTING
        # CREATE SYMBOLIC LINK ON src/ POINTING TO OPTFRAME PROJECT
        # EX: ln -s my/FULL/local/optframe/folder src/optframe-src
        # =========================================================
        'optframe-src': ['*'],
        #
        # OTHER LOCAL FILES ON src/ FOLDER
        # 'Potato': ['*.txt']
    },
    cmdclass={'build_ext': MyBuildExt},
    # packages=find_packages(),  # WHY???
    # THIS DOES NOT WORK FOR C++ REMOTE DEPENDENCY, ONLY PYTHON...
    # install_requires=[
    #    'optframe @ git+https://github.com/optframe/optframe@v4.4', # ONLY WORKS FOR PYTHON PKGS, I GUESS...
    # ]
)
