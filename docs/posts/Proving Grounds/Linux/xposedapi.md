---
title: Xposedapi
date: 2025-04-14
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Xposedapi 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250414224434.png)

Port shows a web page with instructions for an API.

![](../assets/Pasted%20image%2020250414224829.png)

## Initial Access

`/logs` has a WAF, so we can make requests from another host. By using the header `X-Forwarded-For`, we can bypass it.

![](../assets/Pasted%20image%2020250415005047.png)

We see the user `clumsyadmin`; this user can be used in the `/update` endpoint.

Generate a reverse shell with `msfvenom` and start a listener.

![](../assets/Pasted%20image%2020250415005323.png)

Then set a listener and restart the app with `POST /restart`.

![](../assets/Pasted%20image%2020250415005505.png)

![](../assets/Pasted%20image%2020250415005518.png)

Get the flag.

![](../assets/Pasted%20image%2020250415005717.png)

## Privilege Escalation

Search for SUID programs.

![](../assets/Pasted%20image%2020250415005551.png)

![](../assets/Pasted%20image%2020250415005611.png)

![](../assets/Pasted%20image%2020250415005640.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250415005651.png)
