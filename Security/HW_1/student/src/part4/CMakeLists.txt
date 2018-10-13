set(EXECUTABLE_NAME "padding_oracle_attack")
set(PART_NAME "part4")
set(PART_LIB_NAME "PaddingOracleAttack-lib")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${BIN_PATH}/${PART_NAME})
file(GLOB PART_SRC
    "*.cpp")
add_executable(${EXECUTABLE_NAME} ${PART_SRC})

target_link_libraries(${EXECUTABLE_NAME} "EncryptionOracle-lib-part4")

if(BOTAN_FOUND)
  add_dependencies(${EXECUTABLE_NAME} ${BOTAN_LIB_DEP})
  target_link_libraries(${EXECUTABLE_NAME} ${BOTAN_LIBRARY})
endif(BOTAN_FOUND)

add_library(${PART_LIB_NAME} STATIC ${PART_SRC})
add_dependencies(${PART_LIB_NAME} ${BOTAN_LIB_DEP})
