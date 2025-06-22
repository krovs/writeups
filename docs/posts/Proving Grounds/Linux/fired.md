---
title: Fired
date: 2025-04-19
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Fired 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250419170300.png)

At port `9090`, we have an `Openfire` login screen. We search and find the exploit.

## Initial Access

[https://github.com/miko550/CVE-2023-32315](https://github.com/miko550/CVE-2023-32315)

Execute the exploit, create a new user, log in as the user, and upload the jar. Then go to the server tab, server settings, and management tool with password `123`.

![](../assets/Pasted%20image%2020250419184835.png)

![](../assets/Pasted%20image%2020250419192201.png)

![](../assets/Pasted%20image%2020250419192151.png)

Get the flag.

![](../assets/Pasted%20image%2020250419192232.png)

## Privilege Escalation

Find all `openfire` related folders and search for passwords.

![](../assets/Pasted%20image%2020250419205712.png)

![](../assets/Pasted%20image%2020250419205757.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250419205808.png)
