# Copyright (c) <year> <author> (<email>)
# Distributed under the MIT License.
# See accompanying file LICENSE.md or copy at http://opensource.org/licenses/MIT

# Include script to build external libraries with CMake.
include(ExternalProject)

# -------------------------------

ExternalProject_Add(botan-ext
  GIT_REPOSITORY https://github.com/randombit/botan.git
  UPDATE_COMMAND ""
  BUILD_IN_SOURCE 0
  SOURCE_DIR ${EXTERNAL_PATH}/botan-ext
  INSTALL_DIR ${CMAKE_BINARY_DIR}/botan-install
  CONFIGURE_COMMAND ${EXTERNAL_PATH}/botan-ext/configure.py --prefix=${CMAKE_BINARY_DIR}/botan-install
  BUILD_COMMAND make -j4
  INSTALL_COMMAND make install
  BUILD_ALWAYS 0
  )

ExternalProject_Get_Property(botan-ext install_dir)
set(BOTAN_INCLUDE_DIR ${install_dir}/include/botan-2 CACHE INTERNAL "Path to include folder for Botan")
set(BOTAN_LIB_DEP botan-ext)
set(BOTAN_LIBRARY libbotan-2.a)
set(BOTAN_FOUND 1)
message(STATUS "Botan include dir ${BOTAN_INCLUDE_DIR}")

include_directories(SYSTEM AFTER "${BOTAN_INCLUDE_DIR}")
link_directories(${install_dir}/lib)
# -------------------------------
