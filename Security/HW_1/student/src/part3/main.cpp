#include "part3/ECBDecrypt.h"
#include "part3/EncryptionOracle.h"

#include <iostream>

int main() {
  ECBDecrypt d;
  EncryptionOracle e;

  auto secretMessage = d.grader_decrypt(e);
  std::cout << "The secret message is: " << secretMessage << std::endl;
  return 0;
}
