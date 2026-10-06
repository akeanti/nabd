file(GLOB_RECURSE app_sources ${CMAKE_SOURCE_DIR}/src/*.cpp)
idf_component_register(SRCS ${app_sources} INCLUDE_DIRS .)
target_compile_options(${COMPONENT_LIB} PRIVATE $<$<COMPILE_LANGUAGE:CXX>:-std=gnu++17>)
