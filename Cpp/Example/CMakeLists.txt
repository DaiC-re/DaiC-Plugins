cmake_minimum_required(VERSION 3.12)
project(ExampleCpp)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
set(CMAKE_AUTOMOC ON)

add_library(Example MODULE
    Example.cpp)
target_include_directories(Example PRIVATE ./)
target_link_libraries(Example PRIVATE Qt6::Core)
