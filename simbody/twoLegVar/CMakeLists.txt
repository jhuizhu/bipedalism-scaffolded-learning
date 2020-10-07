# Generic CMakeLists.txt for making a Simbody-using executable.
# This shows how to use the provided SimbodyConfig.cmake to locate a Simbody
# installation on your machine so you can use it from your own code.
# You will most likely want to copy some of these lines into your own
# CMakeLists.txt rather than use this one verbatim.
cmake_minimum_required(VERSION 2.8)
project(walker)

# List your source and header files here.
set(my_source_files walker.cpp)

# This depends on SimbodyConfig.cmake being located somewhere predictable
# on your machine. If you have installed it somewhere that CMake won't be
# able to guess, you'll need to tell find_package where to look.
find_package(Simbody REQUIRED)
#set(CMAKE_CXX_FLAGS "-O3")
#set(CMAKE_CXX_FLAGS "-L/users/aas62/opt/usrLocalInclude/lib -I/users/aas62/opt/usrLocalInclude/include -O3")

include_directories(${Simbody_INCLUDE_DIR})
link_directories(${Simbody_LIB_DIR})
## Compiler flags
add_executable(walker.o ${my_source_files} ${my_header_files})
target_link_libraries(walker.o ${Simbody_LIBRARIES} armadillo)
add_executable(walkerVis.o ${my_source_files} ${my_header_files})
set_target_properties (walkerVis.o PROPERTIES COMPILE_DEFINITIONS "VIS_ON")
target_link_libraries(walkerVis.o ${Simbody_LIBRARIES} armadillo)
