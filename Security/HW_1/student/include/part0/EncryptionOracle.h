#ifndef ENCRYPTION_ORACLE_H
#define ENCRYPTION_ORACLE_H

#include <cstdint>
#include <vector>

// DO NOT USE
namespace internal {
  class EncryptionOracle;
};
// DO NOT USE

enum class EncryptionMode { ECB = 0, CBC = 1 };

class EncryptionOracle {
public:

  EncryptionOracle();
  virtual ~EncryptionOracle();


  std::vector<uint8_t> encrypt(std::vector<uint8_t> plaintext);
  std::vector<uint8_t> encryptECB(std::vector<uint8_t> plaintext);

  // DO NOT USE
  EncryptionOracle(internal::EncryptionOracle *e) : internalOracle(e), isExternal(true) {}
  internal::EncryptionOracle *internalOracle;
  bool isExternal;
  // DO NOT USE
};
#endif
