from setuptools import setup, Extension
import subprocess  # IMPORTANT FOR LOCAL GIT CLONE, OR 'ls -la'...
#  https://stackoverflow.com/questions/4529555/building-a-ctypes-based-c-library-with-distutils
from distutils.command.build_ext import build_ext as build_ext_orig
import os

class CTypesExtension(Extension):
    pass

class MyBuildExt(build_ext_orig):
    def run(self):
        subprocess.check_call(
            ['git', 'clone', '--depth', '1', '--branch', '5.1.0', 'https://github.com/optframe/optframe', 'optframe-git'])        
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
            if os.name == 'nt':  # Windows
                # only use .pyd if PyInit_foo() exists...
                return ext_name + '.dll'
            else:
                return ext_name + '.so'
        return super().get_ext_filename(ext_name)

this_directory = os.path.abspath(os.path.dirname(__file__))

my_extra_compile_args = []
# In the future, try c++20. For now, too early.
if os.name == 'posix':  # Linux or macOS
    my_extra_compile_args.append('--std=c++17')
    print("FLAGS for Linux or MacOS")
elif os.name == 'nt':   # Windows
    my_extra_compile_args.append('/std:c++17')
    my_extra_compile_args.append('/DWIN32')
    my_extra_compile_args.append('/D_HAS_STD_BYTE=0')
    print("FLAGS for Windows")
else:
    pass


setup(
    name="optframe",
    version="5.1.0",
    py_modules=["optframe.components","optframe.core","optframe.engine","optframe.heuristics","optframe.protocols"],
    ext_modules=[
        CTypesExtension(
            "optframe.optframe_lib",
            ["optframe/optframe_lib.cpp", "optframe-git/src/OptFrameLib/OptFrameLib.cpp"],
            include_dirs=[os.path.join(
                this_directory, "./optframe-git/include"),
                os.path.join(
                this_directory, "./optframe-git/src")
                ],
            #
            extra_compile_args=my_extra_compile_args
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
    },
    cmdclass={'build_ext': MyBuildExt},
)
