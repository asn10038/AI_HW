#include "part4/PaddingOracle.h"
#include "part4/PaddingOracleAttack.h"
#include <iostream>


int main() {
  PaddingOracle p;
  PaddingOracleAttack a;

  auto plaintext = a.grader_decrypt(p);

  std::cout << "The plaintext is: " << plaintext << std::endl;

  return 0;
}
