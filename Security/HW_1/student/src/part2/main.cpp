#include "part2/CBCDecrypt.h"
#include "part2/EncryptionOracle.h"

#include <iostream>

int main() {
  CBCDecrypt d;
  EncryptionOracle e;

  auto secretMessage = d.grader_decrypt(e);
  std::cout << "The secret message is: " << secretMessage << std::endl;
  return 0;
}
