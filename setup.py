# ===============
# https://github.com/himbeles/ctypes-example/blob/master/setup.py
# https://stackoverflow.com/questions/4529555/building-a-ctypes-based-c-library-with-distutils
# ===============

#
# STEP 1 - VERY GOOD DOCUMENTATION: https://setuptools.pypa.io/en/latest/userguide/ext_modules.html
#

from setuptools import setup, Extension

#  https://stackoverflow.com/questions/4529555/building-a-ctypes-based-c-library-with-distutils
from distutils.command.build_ext import build_ext as build_ext_orig


import os

import subprocess

#from distutils import sysconfig


class CTypesExtension(Extension):
    pass


class build_ext(build_ext_orig):

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
print("MY DIR: ", this_directory)
subprocess.run(["ls", "-l", this_directory+"/src"])

#destination_path = sysconfig.get_python_lib()
# => /usr/lib/python3/dist-packages
#print("DEST PATH: ", destination_path)

setup(
    name="pyoptframe",
    version="1.0.0",
    py_modules=["pyoptframe.demo_pyfcore"],
    ext_modules=[
        CTypesExtension(
            "cpplib.fcore_lib",
            ["cpplib/fcore_lib.cpp"],
            include_dirs=[os.path.join(this_directory, "./src/optframe-src/")],
            extra_compile_args=['--std=c++20']
        ),
    ],
    # package_data includes data from 'src/' folder, by default
    package_data={
        # , 'OptFCore/*', 'OptFCore/FCore.hpp', '*/*', '*/*/*'
        'optframe-src': ['*'],
        # 'Potato': ['*.txt']
    },
    cmdclass={'build_ext': build_ext},
)
