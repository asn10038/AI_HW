#include "part1/ECBDecrypt.h"
#include "part1/EncryptionOracle.h"
#include <iostream>

int main() {
  ECBDecrypt d;
  EncryptionOracle e;

  auto secretMessage = d.grader_decrypt(e);
  std::cout << "The Secret Message is: " << secretMessage << std::endl;
  return 0;
}
