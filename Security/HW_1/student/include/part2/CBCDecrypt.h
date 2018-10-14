#ifndef CBC_DECRYPT_H
#define CBC_DECRYPT_H

#include <string>
#include <vector>

class EncryptionOracle;

class CBCDecrypt {
public:

  std::string grader_decrypt(EncryptionOracle &e);
  /* Checks that the contents of the two are equal to the first n elements */
  bool isNEqual(std::vector<uint8_t> &lhs, std::vector<uint8_t> &rhs, uint n);
  void print_ciphertext(std::vector<uint8_t> ciphertext);
};
#endif
