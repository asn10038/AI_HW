#ifndef ECB_DECRYPT_H
#define ECB_DECRYPT_H

#include <string>

class EncryptionOracle;

class ECBDecrypt {
public:

  std::string grader_decrypt(EncryptionOracle &e);
};
#endif
