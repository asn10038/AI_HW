#include "part4/PaddingOracle.h"
#include "part4/PaddingOracleAttack.h"

#include <assert.h>
#include <iostream>
#include <utility>

#define PRINT(x) std::cout<<x;
#define PRINTL(x) std::cout<<x<<std::endl;

bool PaddingOracleAttack::isNEqual(std::vector<uint8_t> &lhs, std::vector<uint8_t> &rhs, uint n)
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

std::vector<uint8_t> PaddingOracleAttack::XORVector(std::vector<uint8_t> &lhs, std::vector<uint8_t> &rhs)
{
  assert(lhs.size() == rhs.size());
  std::vector<uint8_t> res(lhs.size(), 0);

  for(uint i = 0; i<lhs.size(); i++)
    res[i] = lhs[i]^rhs[i];

  return res;
}


void PaddingOracleAttack::print_ciphertext(std::vector<uint8_t> ciphertext)
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

int PaddingOracleAttack::getNumPadBytes(PaddingOracle &o,
                                        std::vector<uint8_t> &iv,
                                        std::vector<uint8_t> &ciphertext)
{
  /* change bytes until an incorrect padding error occurs */
  std::vector<uint8_t> guess_ciphertext(ciphertext.begin(), ciphertext.end());
  // uint numblocks = guess_ciphertext.size()/blockSize;
  uint blockSize = 16;
  uint SecLastBlockStart = guess_ciphertext.size()-2*blockSize;
  for(uint i=0; i<blockSize; i++)
  {
    if(guess_ciphertext[SecLastBlockStart + i] == 255)
      guess_ciphertext[SecLastBlockStart + i]--;
    else
      guess_ciphertext[SecLastBlockStart + i]++;

    bool flag = o.isValid(iv, guess_ciphertext);
    if(!flag)
    // {
      // PRINTL(i);
      return blockSize-i;
    // } else
    //   PRINTL("valid");

    if(guess_ciphertext[SecLastBlockStart + i] == 254)
      guess_ciphertext[SecLastBlockStart + i]++;
    else
      guess_ciphertext[SecLastBlockStart + i]--;
  }
  return 0;
}

std::vector<uint8_t> PaddingOracleAttack::decryptBlock(PaddingOracle &o, std::vector<uint8_t> &secLastBlock,std::vector<uint8_t> &lastBlock)
{
  uint blockSize = 16;
  /* The value you want the padding bytes to take */
  uint goal = 1;
  uint known_bytes = 0;
  /* the known blockvalues in the key_block */
  std::vector<uint8_t> key_block(blockSize, 0);
  for(uint i=0; i<blockSize; i++)
  {
    /* make the guess_block */
    std::vector<uint8_t> guess_block_ciphertext(secLastBlock.begin(), secLastBlock.end());
    /* for goal number of bytes in guess block */
    for(uint j=1; j<=known_bytes; j++)
    {
      /* change guess value to value that can be xor'd with the key_block */
      /* to get the goal */
      uint8_t num = key_block[blockSize-j] ^ (goal);
      guess_block_ciphertext[blockSize-j] = num;
      assert((guess_block_ciphertext[blockSize-j] ^ key_block[blockSize-j]) == goal);
    }
    uint8_t current_value = guess_block_ciphertext[blockSize-goal];
    bool found_valid = false;
    for(uint j=0; j<256; j++)
    {
      if(j == current_value)
        continue;
      guess_block_ciphertext[blockSize-goal] = j;

      bool valid = o.isValid(guess_block_ciphertext,lastBlock);
      if(valid)
      {
        key_block[blockSize-goal] = goal ^ j;
        std::vector<uint8_t> v = XORVector(key_block, guess_block_ciphertext);
        // print_ciphertext(v);

        known_bytes++;
        goal++;
        found_valid = true;
        break;
      }

    }
    /* Enter this if statement if you've hit the real padding value */
    /* Should probably add some check of correctness here */
    if(!found_valid){
      guess_block_ciphertext[blockSize-goal] = current_value;
      assert(o.isValid(guess_block_ciphertext, lastBlock));
      key_block[blockSize-goal] = goal^current_value;
      std::vector<uint8_t> v = XORVector(key_block, guess_block_ciphertext);
      // print_ciphertext(v);
      known_bytes++;
      goal++;
      found_valid = true;
    }
  }
  std::vector<uint8_t> decrypted_block = XORVector(key_block, secLastBlock);
  // print_ciphertext(decrypted_block);
  //
  // PRINT("NUM KNOWN BYTES: ");
  // PRINTL(known_bytes);
  return decrypted_block;
}

std::string PaddingOracleAttack::grader_decrypt(PaddingOracle &o) {
  // NOTE: Please write your code here.
  uint blockSize = 16;
  std::pair<std::vector<uint8_t>, std::vector<uint8_t>> pair = o.encrypt();
  std::vector<uint8_t> iv = std::get<0>(pair);
  std::vector<uint8_t> ciphertext = std::get<1>(pair);

  /* This is initialization code done in a dumb way. Too lazy to fix */
  std::vector<uint8_t> lastBlock(ciphertext.begin(), ciphertext.begin()+16);
  std::vector<uint8_t> secLastBlock(ciphertext.begin(), ciphertext.begin()+16);
  /* ---------------------------------------------------------------------- */

  /* ------------------------- */
  /* Need to iterate through all the blocks and IV */
  assert(ciphertext.size()%blockSize==0);
  uint num_blocks = ciphertext.size()/blockSize;
  // print_ciphertext(ciphertext);
  std::vector<uint8_t> plaintext;
  for(int i=num_blocks; i>0; i--)
  {
    uint8_t lastBlockEnd = blockSize*i;
    uint8_t lastBlockBegin = lastBlockEnd - blockSize;


    std::vector<uint8_t> lastBlock(ciphertext.begin() + lastBlockBegin,
                                   ciphertext.begin() + lastBlockEnd);
    /* use the IV for the first block */
    if(i != 1)
    {
      uint8_t secLastBlockEnd = lastBlockEnd - blockSize;
      uint8_t secLastBlockBegin = lastBlockBegin - blockSize;
      secLastBlock = std::vector<uint8_t>(ciphertext.begin() + secLastBlockBegin,
                   ciphertext.begin() + secLastBlockEnd);
    } else {
      secLastBlock = iv;
    }

    std::vector<uint8_t> decrypted_block = decryptBlock(o, secLastBlock, lastBlock);
    plaintext.insert(plaintext.end(), decrypted_block.begin(), decrypted_block.end());
    // print_ciphertext(decrypted_block);
    // PRINTL(" ");
  }
  print_ciphertext(plaintext);
  for(uint i=0; i<plaintext.size(); i++)
  {
    PRINT(unsigned(plaintext[i]));
    PRINT(" --> ");
    PRINTL(plaintext[i]);
  }



  return "";
}
