# Copyright (c) <year> <author> (<email>)
# Distributed under the MIT License.
# See accompanying file LICENSE.md or copy at http://opensource.org/licenses/MIT

cmake_minimum_required(VERSION 2.6)
set(CMAKE_CXX_STANDARD 11)

set(PROJECT_NAME "homework1")

# Change this section to correspond with your project info.
project(${PROJECT_NAME} C CXX)
set(PROJECT_PATH                               "${CMAKE_CURRENT_SOURCE_DIR}")
set(INCLUDE_PATH                               "${PROJECT_PATH}/include")
set(PROVIDED_PATH                              "${PROJECT_PATH}/provided")
set(SRC_PATH                                   "${PROJECT_PATH}/src")
if(NOT EXTERNAL_PATH)
  set(EXTERNAL_PATH                            "${PROJECT_PATH}/external")
endif(NOT EXTERNAL_PATH)
set(BIN_PATH                                   "${PROJECT_BINARY_DIR}/bin")

include(CMakeDependentOption)

set(CMAKE_BUILD_TYPE STREQUAL "Debug")
set(CMAKE_CXX_FLAGS
  "${CMAKE_CXX_FLAGS} -Wall")

if(CMAKE_COMPILER_IS_GNUCXX)
    set(CMAKE_CXX_FLAGS_DEBUG   "-O0 -g3")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif(CMAKE_COMPILER_IS_GNUCXX)

include(Dependencies.cmake)
include_directories(AFTER "${INCLUDE_PATH}")
link_directories("${PROVIDED_PATH}/lib")

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${LIB_PATH})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${LIB_PATH})

add_subdirectory(src)

add_custom_command(OUTPUT ${PROJECT_NAME}_submission.tar.xz
  COMMAND tar cfJ ${PROJECT_NAME}_submission.tar.xz ${SRC_PATH}
  COMMENT "Generating Submission Archive"
)

add_custom_target(submission-archive ALL DEPENDS ${PROJECT_NAME}_submission.tar.xz)
