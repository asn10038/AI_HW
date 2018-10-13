#ifndef CBC_DECRYPT_H
#define CBC_DECRYPT_H

#include <string>

class EncryptionOracle;

class CBCDecrypt {
public:

  std::string grader_decrypt(EncryptionOracle &e);
};
#endif
