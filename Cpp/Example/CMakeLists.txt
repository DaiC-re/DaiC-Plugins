cmake_minimum_required(VERSION 3.12)
project(Example)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
set(CMAKE_AUTOMOC ON)

add_library(Example MODULE
    Example.cpp)
  target_include_directories(Example PRIVATE ./../../../DaiCCore/include/Plugins/)
target_link_libraries(Example PRIVATE Qt6::Core)
set_target_properties(Example PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}
)
install(TARGETS Example
        DESTINATION ${CMAKE_INSTALL_PREFIX})
