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
There are US export controls on cryptography. There needs to be a license to export confidential technology. Authentication technology is not restricted.

#### b) What area of expertise was lacking in the in-person IETF meetings on IPsec?
The designers had a somewhat limited cryptographic knowledge.

#### c) What was the explanation for having sequence numbers in swipe?
They were included "to protect against replay" attacks.

#### d)  What benefit did sequence numbers end up providing IP sec?
They were used to prevent malicious retransmission of packets.  

#### e) Skip was proposed by who? and why wasn't it chosen?
Skip was proposed by Sun, and it wasn't chosen because it didn't allow for a change in Diffie Helman parameters. Sun had recently had a problem with choosing bad DH parameters.


### 4) The chrome browser and usability

#### a) What are the steps a user must perform to see the contents of stored cookies?
settings -> advanced_settings -> privacy and security -> content settings -> cookies -> see all cookies and site data -> click on particular cookie to see content

#### b) How would you re design this so the user can 1) easily see the contents of cookies and 2) reduce the number of steps to get to the point where the cookies are
To address concern \#2 I would put a link to the view cookies page in the dropdown where the settings link is.
To address concern \#1  I think they actually do an ok job at this, but it's all stored in local storage. Making it accessible via the default file system viewer would be a nice touch. Also if there were an alert with all the cookie data any time a website added something to persistent local storage I think that would make the data easier to digest. One at a time rather than a giant block.

#### c) What are handlers and why are they there? Why are they dangerous?
There are many different types of links on the internet with different types of protocols. The most common protocol http/https is and should be supported by the browser. Links that return types of information that the browser can't understand like email links, calendar links with other unusual protocols need to be handled by other applications. Not the browser. As such chrome allows users to add handlers that automatically open these other applications for these other types of links. The default is to allow this behavior because most people just want to click and open the content. They don't really care what opens it.
On the web whenever a email address is listed usually it contains a mailto: protocol link. When a user clicks on this usually a new email screen appears with the links associated email address in the to section. What's special about this is that the new email screen is in the users email client not the browser. If one were to disable the handlers this interaction could not take place.

The risk here is that handlers provide links a way to get outside the sandbox of the browser. Usually activity in the browser is restricted to the browser. Now attackers have a way to exploit this handler feature to further exploit another application.

### 5) How do requirements placed on passwords contribute to the insecurity of the password? -- UNSURE
 Users will always do the bare minimum effort required. As such the passwords minimum requirements need to be secure. However poor usability often means poor security, and users will find workarounds if security measures are too inconvenient. When users find workarounds the whole system's security suffers.


### 6) Find an article describing failure rates or issues with facial recognition as a method of authentication?
On the vulnerability of face recognition systems towards morphed face attacks authored by:
Ulrich Scherhag et al.
www.researchgate.net/publication/317245046_On_the_vulnerability_of_face_recognition_systems_towards_morphed_face_attacks

This particular paper deals with attacks in which someone is presenting a form of identification in which they control the image on the ID. The verification system is then processing if the photo presented looks like the person presenting the photo. The particular attack they deal with is the "morphed face attack". The scenario they use as an example is immigration.

In many countries to get a passport one submits a photo which is then scanned and passed to the passport creation office. In this scenario the morphed face attack takes place as follows. Person A is able to travel and has a clean record while person B is on the no fly list for any number of reasons. Person A submits a photo and gets a legitimate passport. Person B uses the passport. Normally this attack is prevented because person A and B don't look alike both to people and to computers. However in a morphed face attack the photo that person A submitted is a photo containing features of both A and B's face. So the resulting photo looks something like both people. A human will notice that it's not exact, but given some explaining and given people A and B probably look somewhat similar anyway it's easy to understand a human may not catch this. The question is whether or not a facial recognition system will. One way to think of this would be a hash collision. Both people map to the same document.

This paper doesn't implement a new version of this attack or propose this attack but evaluates the effectiveness of this attack with different facial recognition systems. They also put together a new dataset of morphed faces and originals for others to use.

In their evaluation they examine the effect of morphed face attacks on 2 different facial recognition systems. The first was the commercial VeriLook SDK and the other was the opensourced OpenFace. They also ran their experiments with both HP and Ricoh scanned images as well as the original.

The success of this attack in their charts and figures is somewhat ambiguous. They found that using Veriface with the original scanned images, HP scanned images, and RICOH scanned images had a attack success probability of 100%, 99.7%, and 97.3% respectively. With OpenFace SDK they found the chances of the attack succeeding in the same order was 80.1%, 62.3%, 70.8%. While I think that these numbers are a bit inflated they are high enough to show that there is a real probability that morphed face attacks could be successful.

### 7) What main issues are the papers addressing? Summarize the experiments about what worked and did not work for addressing this issue.

These 3 papers tackle related challenges under the same umbrella problem. There is almost always a tradeoff between security and usability. The risk is in the fact that when you amp up security at the expense of usability users develop a callousness to security warnings. They tend to just ignore them put them off etc. In the end this makes the system both insecure and unusable. These papers approach some guidelines/warnings to approach this problem.

 









### Describe the POODLE attack
