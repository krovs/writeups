---
title: Dvr4
date: 2025-04-22
categories:
- Proving Grounds
- Windows
tags:
- Proving Grounds
- Windows
---


# Dvr4 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250422203804.png)

Web page at port `8080` shows an `Argus Surveillance` web.

![](../assets/Pasted%20image%2020250422205104.png)

There is a path traversal vulnerability.

![](../assets/Pasted%20image%2020250422205523.png)

## Initial Access

We have two users; we can try `id_rsa` keys.

![](../assets/Pasted%20image%2020250422234443.png)
![](../assets/Pasted%20image%2020250422235242.png)
![](../assets/Pasted%20image%2020250422235347.png)

Get the flag.

![](../assets/Pasted%20image%2020250422235451.png)

## Privilege Escalation

Searching for `argus` vulns, we see the weak password encryption.

![](../assets/Pasted%20image%2020250423101858.png)

So we get the administrator hash.

![](../assets/Pasted%20image%2020250423101910.png)
![](../assets/Pasted%20image%2020250423102055.png)

We have `14WatchD0g` and `ImWatchingY0u`.

The last character is missing, and looking at the code it says...

![](../assets/Pasted%20image%2020250423113753.png)

So we can try all special characters.

![](../assets/Pasted%20image%2020250423113824.png)
![](../assets/Pasted%20image%2020250423113834.png)

Now try `psexec`.

![](../assets/Pasted%20image%2020250423113852.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250423113907.png)
