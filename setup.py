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

# trying this... https://stackoverflow.com/questions/59772476/how-to-write-setup-py-to-include-a-specific-git-repo-as-a-dependency
# this seems to require 'find_packages' and install_requires for remote git.... let's see!


#  https://stackoverflow.com/questions/4529555/building-a-ctypes-based-c-library-with-distutils
from distutils.command.build_ext import build_ext as build_ext_orig


import os


# from distutils import sysconfig


class CTypesExtension(Extension):
    pass


class MyBuildExt(build_ext_orig):
    # 'run' from: https://stackoverflow.com/questions/45599346/ask-setuptools-to-git-clone-c-repository
    def run(self):
        subprocess.check_call(
            ['git', 'clone', '--depth', '1', '--branch', 'master', 'https://github.com/optframe/optframe', 'optframe-git'])
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

# destination_path = sysconfig.get_python_lib()
# => /usr/lib/python3/dist-packages
# print("DEST PATH: ", destination_path)

setup(
    name="pyoptframe",
    version="1.0.0",
    py_modules=["pyoptframe.demo_pyfcore"],
    ext_modules=[
        CTypesExtension(
            "cpplib.fcore_lib",
            ["cpplib/fcore_lib.cpp"],
            #include_dirs=[os.path.join(this_directory, "./src/optframe-src/")],
            include_dirs=[os.path.join(
                this_directory, "./optframe-git/include")],
            extra_compile_args=['--std=c++17', '-fconcepts']
        ),
    ],
    # package_data includes data from 'src/' folder, by default
    package_data={
        # , 'OptFCore/*', 'OptFCore/FCore.hpp', '*/*', '*/*/*'
        'optframe-src': ['*'],
        # 'Potato': ['*.txt']
    },
    cmdclass={'build_ext': MyBuildExt},
    # packages=find_packages(),  # WHY???
    # install_requires=[
    #    'optframe @ git+https://github.com/optframe/optframe@v4.4', # ONLY WORKS FOR PYTHON PKGS, I GUESS...
    # ]
)
