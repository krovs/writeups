---
title: Pc
date: 2025-03-27
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Pc 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250327233959.png)

## Initial Access

Going to port `8000`, we are in a terminal.

![](../assets/Pasted%20image%2020250327234109.png)

## Privilege Escalation

We can see a script that opens port `65432`.

![](../assets/Pasted%20image%2020250328102815.png)

![](../assets/Pasted%20image%2020250328102846.png)

Looking at the code, this is an `RPC` app.

![](../assets/Pasted%20image%2020250328121400.png)

Searching for `rpc` exploits:

[https://github.com/ehtec/rpcpy-exploit](https://github.com/ehtec/rpcpy-exploit)

Change the payload to `chmod +s /bin/bash`.

![](../assets/Pasted%20image%2020250328132039.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250328132121.png)
