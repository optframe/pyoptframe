cmake_minimum_required(VERSION 3.27)
project(pyoptframe-project LANGUAGES CXX VERSION 0.0.1)
#
set (CMAKE_CXX_STANDARD 17)
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_CXX_EXTENSIONS OFF)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
Include(FetchContent)

# ====== configure project with header only library ======
add_library(OptFrameAll INTERFACE)
target_include_directories(OptFrameAll INTERFACE thirdparty/optframe-external/include/)

# This will simply test if 'thirdparty/optframe-external' is working
add_executable(app_demo_opt_py thirdparty/optframe-external/demo/00_SimpleBuild/src/OptFCore_load.cpp)
target_link_libraries(app_demo_opt_py PRIVATE OptFrameAll)

# ==================================
# trying to build .so / .dll library

# Create the shared library
add_library(optframe_lib MODULE optframe/optframe_lib.cpp thirdparty/optframe-external/src/OptFrameLib/OptFrameLib.cpp)
target_link_libraries(optframe_lib PRIVATE OptFrameAll)

# Set the output directory for the shared library
set_target_properties(optframe_lib PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/optframe
    LIBRARY_OUTPUT_NAME optframe_lib
    WINDOWS_EXPORT_ALL_SYMBOLS ON
    POSITION_INDEPENDENT_CODE ON
)
# https://stackoverflow.com/questions/58059048/ambiguous-byte-definition-in-rpcndr-and-cstddef#58060367
target_compile_definitions(optframe_lib PRIVATE _HAS_STD_BYTE=0)

# use 'make' to build .so file, instead of this!

