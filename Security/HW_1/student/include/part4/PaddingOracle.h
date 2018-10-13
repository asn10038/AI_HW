#ifndef PADDING_ORACLE_H
#define PADDING_ORACLE_H

#include <cstdint>
#include <vector>

// DO NOT USE
namespace internal {
  class PaddingOracle;
};
// DO NOT USE


class PaddingOracle {
public:

  PaddingOracle();
  virtual ~PaddingOracle();

  bool isValid(std::vector<uint8_t> iv, std::vector<uint8_t> ciphertext);
  // First is iv, Second is ciphertext.
  std::pair<std::vector<uint8_t>, std::vector<uint8_t>> encrypt();

  // DO NOT USE
  PaddingOracle(internal::PaddingOracle *o) : internalOracle(o), isExternal(true) {}
  internal::PaddingOracle *internalOracle;
  bool isExternal;
  // DO NOT USE
};
#endif
