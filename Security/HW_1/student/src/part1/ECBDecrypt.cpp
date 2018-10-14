#include "part1/ECBDecrypt.h"
#include "part1/EncryptionOracle.h"
#include <iostream>
#include <assert.h>

#define PRINT(x) std::cout<<x;
#define PRINTL(x) std::cout<<x<<std::endl;

void ECBDecrypt::print_ciphertext(std::vector<uint8_t> ciphertext)
{
  uint8_t size = ciphertext.size();
  uint blockSize = 16;
  if(size % blockSize != 0)
    PRINTL("THERE IS AN ERROR");

  for(int i=0; i<size; i++)
  {

    PRINT(unsigned(ciphertext[i]));
    PRINT(" ")
    if(i%16 == 15)
      PRINT("\n");
  }
  PRINT("-------------------------\n")
}

/* Checks that the contents of the two are equal to the first n elements */
bool ECBDecrypt::isNEqual(std::vector<uint8_t> &lhs, std::vector<uint8_t> &rhs, uint n)
{
  for(uint i=0; i<n; i++)
  {
    if(lhs[i] != rhs[i])
    {
      return false;
    }
  }
  return true;

}

std::string ECBDecrypt::grader_decrypt(EncryptionOracle &e) {
  // NOTE: Please write your code here.
  // size_t bufsize = 1;
  uint blockSize = 16;
  uint8_t alphabet[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                    '1','2','3','4','5','6','7','8','9','0',',','.','!',' ','$' };

  std::string postfix;

  int tmp = 0;
  while(true)
  {

    /*integer floor division*/
    uint numblocks = postfix.size()/16;

    uint goal = numblocks*16+15;
    uint numAs = goal-postfix.size();

    // controlBuffer looks like [AAAA...] but if you append the postfix it should line up with the known portion of postfix
    std::vector<uint8_t> controlBuffer(numAs, 'A');

    std::vector<uint8_t> postfixBuffer(postfix.begin(), postfix.end());
    std::vector<uint8_t> buffer;

    buffer.insert(buffer.begin(), controlBuffer.begin(), controlBuffer.end());
    buffer.insert(buffer.end(), postfixBuffer.begin(), postfixBuffer.end());


    //push an extra character at the end that will be the guess character
    buffer.push_back('A');
    // buffer at this point looks like [AAA...postfixA]...total length should be a multiple of block size
    assert(buffer.size()%blockSize == 0);

    std::vector<uint8_t> control_ciphertext = e.encrypt(controlBuffer);

    bool found = false;
    for (uint i=0; i<sizeof(alphabet); i++)
    {
      char guess = alphabet[i];
      buffer[buffer.size()-1] = guess;
      std::vector<uint8_t> guess_ciphertext = e.encrypt(buffer);

      if(isNEqual(control_ciphertext, guess_ciphertext, buffer.size()))
      {
        found = true;
        postfix.push_back(guess);
        break;
      }
    }
    /* When there is nothing left to be found breaking the loop.
      This is a dumb way to do it, but it's the easiest
      */
    if(!found)
      break;
    tmp++;
  }

  return postfix;
}
