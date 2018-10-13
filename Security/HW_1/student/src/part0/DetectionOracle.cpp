#include "part0/DetectionOracle.h"
#include "part0/EncryptionOracle.h"
#include <iostream>
/* NOTE: Any Botan header can be included as follows:
   #include <botan/nameofheader.h>
*/

#define PRINT(x) std::cout<<x<<std::endl;
uint32_t DetectionOracle::grader_detectBlockSize(EncryptionOracle &e) {
  // NOTE: For this part use the `encryptECB()` method of the `EncryptionOracle`
  // (ie. e.encryptECB(plaintext) )
  // NOTE: Once you determine the block size, you may assume said size for the rest of the assignment.

  /* Determining the block size can be done by feeding in plain text of different fixed lengths,
     and when the block size is changed it will change by the block size */
  // int blockSize = 0;
  // int currentGuess = 0;

    size_t bufsize = 1;
    std::vector<uint8_t> buffer(bufsize, 'A');
    std::vector<uint8_t> ciphertext = e.encryptECB(buffer);
    int outLength = ciphertext.size();

  return outLength;
}

EncryptionMode DetectionOracle::grader_detectMode(EncryptionOracle &e) {
  // NOTE: For Example Purposes. Only shown in `part0``.
  // If in doubt always refer to the `includes` directory
  // at the top of the repository for more information (ie. function signatures, types, etc).
  // Please ignore the `internal` namespace.

  int blockSize = grader_detectBlockSize(e);
  size_t bufsize = blockSize * 2-1;


  // In ECB mode the same plain text will always produce the same ciphertext.
  // Therefore we should send two block size
  std::vector<uint8_t> buffer(bufsize, 'A');
  // std::cout << "bufsize is: " << buffer.size() << std::endl;

  std::vector<uint8_t> ciphertext = e.encrypt(buffer); // NOTE: Mind the use of `encrypt()` in this function.

  std::vector<uint8_t> blockOne(ciphertext.begin(), ciphertext.begin()+blockSize);
  std::vector<uint8_t> blockTwo(ciphertext.begin()+blockSize, ciphertext.end() );

  // std::string str(blockOne.begin(), blockOne.end() );
  // PRINT(ciphertext.size());
  // PRINT(blockOne.size());
  // std::string str2(blockTwo.begin(), blockTwo.end() );
  // PRINT(blockTwo.size());

  if(blockOne.size() == blockTwo.size())
    return EncryptionMode::ECB;
  return EncryptionMode::CBC;

  return EncryptionMode::CBC;
}
