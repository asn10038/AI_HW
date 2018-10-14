#ifndef ECB_DECRYPT_H
#define ECB_DECRYPT_H

#include <string>
#include <vector>

class EncryptionOracle;

class ECBDecrypt {
public:

  std::string grader_decrypt(EncryptionOracle &e);
  void print_ciphertext(std::vector<uint8_t> ciphertext);

  /* Checks that the contents of the two are equal to the first n elements */
  bool isNEqual(std::vector<uint8_t> &lhs, std::vector<uint8_t> &rhs, uint n);
};
#endif
