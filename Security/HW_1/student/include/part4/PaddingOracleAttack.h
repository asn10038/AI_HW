#ifndef PADDING_ORACLE_ATTACK_H
#define PADDING_ORACLE_ATTACK_H

#include <string>
#include <vector>

class PaddingOracle;

class PaddingOracleAttack {
public:
  bool isNEqual(std::vector<uint8_t> &lhs, std::vector<uint8_t> &rhs, uint n);
  void print_ciphertext(std::vector<uint8_t> ciphertext);
  std::string grader_decrypt(PaddingOracle &o);

  int getNumPadBytes(PaddingOracle &o, std::vector<uint8_t> &iv, std::vector<uint8_t> &ciphertext);

  std::vector<uint8_t> XORVector(std::vector<uint8_t> &lhs, std::vector<uint8_t> &rhs);

  std::vector<uint8_t> decryptBlock(PaddingOracle &o, std::vector<uint8_t> &secLastBlock, std::vector<uint8_t> &lastBlock);

};
#endif
