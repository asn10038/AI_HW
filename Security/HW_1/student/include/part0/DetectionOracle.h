#ifndef DETECTION_ORACLE_H
#define DETECTION_ORACLE_H

#include <botan/block_cipher.h>
#include <botan/cipher_mode.h>
#include <botan/hex.h>
#include <fstream>
#include <cstdint>

class EncryptionOracle;
enum class EncryptionMode;

class DetectionOracle {
public:
  uint32_t grader_detectBlockSize(EncryptionOracle &e);

  EncryptionMode grader_detectMode(EncryptionOracle &e);
};
#endif
