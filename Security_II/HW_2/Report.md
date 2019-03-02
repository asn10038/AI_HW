# HW 2 Security II
---

### 1) What issues have prevented the deployment of TLS 1.3 and why has the RFC been redrafted a bunch of times?

Like most things in cryptology when ideas are implemented in practice things tend to go wrong. In this case, when TLS 1.3 was implemented it became clear that it is
incompatible with the the way the internet evolved over time.

Because there are so many devices supporting different levels of security on the internet, browsers needed
to support multiple versions of TLS. Therefore the server could force a connection with an older security protocol if that's all it supported and the client would connect just with a slower startup time. This wasn't a problem until it became clear that an attacker can force a downgrade by pretending the server only supported an older protocol. The problem was exploited by a vulnerability found in an older security protocol SSLv3. Luckily it isn't widely used and support for it has mostly been removed. While this particular attack has been mostly mitigated, it proves that downgrade attacks are a real concern and designers have to prepare for them.

This insecure downgrading was removed and the community felt it was time to release 1.3 again. Unfortunately most servers didn't implement this version negotiation properly and 1.2 servers would disconnect instead of negotiating. This created the same problem as originally. Clients would have allow an insecure downgrade. To resolve this the RFC was rewritten again with a new an improved version negotiation that treats 1.3 as a protocol upgrade rather than the default.

Again this seemed to solve the problem, and it did for most clients and servers. Unfortunately there are a lot of other boxes that need to deal with TLS to move packets from client to server. They weren't programmed with these changes in mind or that these changes might happen, and caused connections to fail. (Some reasons for the connection failures included 1.3 removing fields that were considered essential) 1.3/1.2 in theory aren't the problem. It's the fact that it is incompatible with the way 1.2 was implemented. And so, the RFC was redrafted in a way that 1.3 appeared like 1.2 not only to clients and servers but also middleboxes. This included re introducing fields back into the server hello message. Since then the RFC has been consistently redrafted to support middleboxes.

In the end the reasons the RFC has been re written so many times is twofold. 1) It's been shown that downgrade attacks are real and dangerous. 2) Implementing an upgrade that prevents these downgrade attacks and remains compatible with everything that's on the internet is really hard.   

### 2) Describe the POODLE attack
POODLE is a type of downgrade attack. While most of the internet uses TLS 1.3 1.2 and 1.1 most clients and servers supported the older SSLv3 protocol. It is the predecessor to the TLS protocols and in order to keep new machines compatible with older machines the newer protocols were designed to allow for the older forms of communication.
This wasn't considered a problem because there was no severe issue with the SSLv3 protocol. This is no longer true.

POODLE works by first exploiting this downgrading property and then exploiting a flaw SSLv3's CBC encryption. The flaw is that the block cipher padding
is non deterministic and not covered by the MAC. This means the integrity of the padding cannot be determined during encryption making it an attack vector.
If the attacker swaps blocks in the message they can learn information about the plain text based on weather or not the message is still accepted as if it had the right padding. This leads to a padding oracle attack. If the encrypted text is selected it leaks information about 1 byte of plain text. Working backwards the attacker can then decrypt the entire message.

In detail this works by exploiting the padding scheme. For a block with 1 byte of padding the value of the last byte is 1. Given K is a block in the sequence, if the attacker crafts a request that gets accepted it knows that D(k-1) XOR K = 1. This now leaks what the value of the last byte of K-1 is. The attacker can create a last block full of padding which functions a K with known values. The attacker can then work incrementally backwards until the whole message is decrypted. The attack works a byte at a time so there's only 256 values to search. This makes the attack feasible.

The only thing left for the attacker to figure out is how big the actual payload is since the original padding hides the actual length of the payload and the attacker needs control of the last block. The attacker can then send requests of increasing length until a block boundary is crossed and the server responds with an extra encrypted block.

So in summary the attack works as follows:
1) The attacker acts as the man in the middle of a normal cookie bearing client server interaction to gain access to the cookie
2) The malicious client manipulates the TLS protocol to downgrade to SSLv3
3) The attacker can send specialized requests to the server that decrypt the cookie byte by byte

### 3) IPSec History Lecture
#### a) How did politics contribute to IPsec having an integrity only option (AH)?
There was an argument over whether they should use the ESP/AH setup a stateful protocol or SKIP a stateless protocol. As such when people are split on technical decisions political motivations make the decision. SKIP was backed by Sun which had an issue with bad Diffie Helman parameters and SKIP didn't allow for changing DH parameters. Ultimately ESP/AH was picked and because of how expensive encryption was on the hardware at the time AH (integrity only) was a rational compromise.

#### b) What area of expertise was lacking in the in-person IETF meetings on IPsec?


















### Describe the POODLE attack
