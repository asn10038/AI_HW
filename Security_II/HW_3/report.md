# Homework 3 Report
---
### Damballa RN DGA's Case Study Summary
The case study covers Malware that use Domain Generation algorithms to bypass domain blacklists. Attackers change the domains associated with the command and control servers so that AV can't block the requests. The particular malware that was uncovered in this case study was a Zeus v3 variant that used Peer to Peer as its primary command-and-control mechanism but used DGA domains if it failed.

Damballa began tracking down the malware by monitoriing nonexistent domain name responses (NXDomains).  After a list of fake domains was compiled they were clustered and mapped back to the registered domains used by the attackers. Damballa continued to work backwards to find exploit sites, redirector domains, and the original spam messages. 

After clustering they tagged the clusters as either *Known Malicious* or *Unknown*. DGA's generate thousands of domains per week so tackling the problem at this scale is untenable by human users. 

After clustering, to track the original C&C server Damballa associated the many domain names with only a few ip addresses. An email address is associated with all domain names so they looked up the associated email address and found a few domains associated with the email address. Once the questionable sites were tracked down it was easy to get a copy of the malware for analysis and verify that the domains caught by the clustering algorithm were indeed related to this particular malware. Checking the malicious distribution domains Damballa found this malware was spread via Better Business Bureau and NACHA spamming campaigns.

The malware was an executable meant for a Windows 7 64 bit environment, and was downloaded into ...\AppData\Roaming. By putting it in this folder it meant that on an enterprise system this executable would remain available regardless of the machine every time the user logged in. The malware also created firewall rules, and autostart registry entries so that the malware could function correctly. To avoid AV the malware is polymorphic, meaning that the actualy contents vary but the function remains the same. The intent of the malware is to steal banking information and then exfiltrate that info via encrypted HTTP POST requests. The first attempt to connect to the botnet and the criminal operator is to use P2P connections. If none are available it resorts to  domain generation. The malware uses the data as the seed for the random domains.

