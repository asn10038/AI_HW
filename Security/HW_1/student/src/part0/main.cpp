#include "part0/DetectionOracle.h"
#include "part0/EncryptionOracle.h"
#include <iostream>

/* NOTE: You may modify this code for your testing.
   Modifications will not be submitted as part of the assignment.
*/
int main() {
  DetectionOracle o;
  EncryptionOracle e;

  auto mode = o.grader_detectMode(e);
  auto blockSize = o.grader_detectBlockSize(e);
  std::cout << "Detected Block Size: " << blockSize << std::endl;
  std::cout << "Detected Mode: " << static_cast<int>(mode) << std::endl;

  return 0;
}
