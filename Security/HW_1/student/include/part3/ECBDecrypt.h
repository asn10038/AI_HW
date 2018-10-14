#ifndef ECB_DECRYPT_H
#define ECB_DECRYPT_H

#include <string>
#include <vector>

class EncryptionOracle;

class ECBDecrypt {
public:

  int find_prefix_length(EncryptionOracle &e);
  std::string grader_decrypt(EncryptionOracle &e);
  bool isNEqual(std::vector<uint8_t> &lhs, std::vector<uint8_t> &rhs, uint n);
  void print_ciphertext(std::vector<uint8_t> ciphertext);
};
#endif
