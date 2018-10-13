#ifndef PADDING_ORACLE_ATTACK_H
#define PADDING_ORACLE_ATTACK_H

#include <string>

class PaddingOracle;

class PaddingOracleAttack {
public:
  std::string grader_decrypt(PaddingOracle &o);
};
#endif
