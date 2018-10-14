#include "part3/ECBDecrypt.h"
#include "part3/EncryptionOracle.h"
#include <assert.h>
#include <iostream>

#define PRINT(x) std::cout<<x;
#define PRINTL(x) std::cout<<x<<std::endl;

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


int ECBDecrypt::find_prefix_length(EncryptionOracle &e)
{
  uint blockSize = 16;
  uint num_blocks;
  uint filler_length = 0;
  /* the two equal blocks */
  uint block2;
  bool found = false;
  uint ret = 0;

  while(true)
  {
    std::vector<uint8_t> controlBuffer(filler_length, 'A');
    std::vector<uint8_t> ciphertext = e.encrypt(controlBuffer);
    // print_ciphertext(ciphertext);
    assert(ciphertext.size() % blockSize == 0);
    num_blocks = ciphertext.size()/blockSize;

    /* make sure num_blocks total > 1 */
    if(num_blocks < 1)
      continue;

    /* search for identical blocks */
    for(uint j=1; j<num_blocks; j++)
    {
      uint startBlock1 = blockSize*(j-1);
      uint startBlock2 = blockSize*j;
      std::vector<uint8_t> v1(ciphertext.begin()+startBlock1,
                              ciphertext.begin()+startBlock1 + blockSize);
      std::vector<uint8_t> v2(ciphertext.begin()+startBlock2,
                              ciphertext.begin()+startBlock2 + blockSize);

      if(isNEqual(v1, v2, v1.size()))
      {
        block2 = j;
        found = true;
        break;
      }
    }
    if(found)
    {
      /* Know the blocks look like this
        [prefixAAAA...][AAAA...AA][AAAA...AA][postfix]
       */

      /* calculate the prefix length */
      /* need to add one because block1 is indexed at 0
         so the first 16 bytes don't get counted in the math */
      uint total_bytes = blockSize*(block2+1);
      // PRINTL(filler_length);
      ret = total_bytes - filler_length;
      break;
    }
    filler_length++;

  }

  // PRINT("BLOCK 1: ");
  // PRINTL(block1);
  // PRINT("BLOCK 2: ");
  // PRINTL(block2);
  return ret;
}



std::string ECBDecrypt::grader_decrypt(EncryptionOracle &e) {
  // NOTE: Please write your code here.
  uint prefix_length = find_prefix_length(e);
  PRINT("PREFIX LENGTH: ");
  PRINTL(prefix_length);

  //
  uint blockSize = 16;
  uint8_t alphabet[] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                        '1','2','3','4','5','6','7','8','9','0',',','.','!',' ','$', '\'', ';','@', '#', '%', '\t', '\n' };

  std::string postfix;

  while(true)
  {
    uint numblocks = (prefix_length + postfix.size()) / 16;
    uint goal = numblocks*16+15;
    uint numAs = goal - postfix.size() - prefix_length;

    std::vector<uint8_t> controlBuffer(numAs, 'A');

    std::vector<uint8_t> postfixBuffer(postfix.begin(), postfix.end());
    std::vector<uint8_t> buffer;

    buffer.insert(buffer.begin(), controlBuffer.begin(), controlBuffer.end());
    buffer.insert(buffer.end(), postfixBuffer.begin(), postfixBuffer.end());


    //push an extra character at the end that will be the guess character
    buffer.push_back('A');
    // buffer at this point looks like [AAA...postfixA]...total length + pref should be a multiple of block size
    assert((buffer.size()+prefix_length)%blockSize == 0);

    std::vector<uint8_t> control_ciphertext = e.encrypt(controlBuffer);
    print_ciphertext(control_ciphertext);
    bool found = false;

    for (uint i=0; i<sizeof(alphabet); i++)
    {
      char guess = alphabet[i];
      buffer[buffer.size()-1] = guess;
      std::vector<uint8_t> guess_ciphertext = e.encrypt(buffer);
      if(isNEqual(control_ciphertext, guess_ciphertext, goal))
      {
        found = true;
        postfix.push_back(char(guess));
        break;
      }
    }
    if(!found)
    {
      break;
    }
  }

  return postfix;
}
