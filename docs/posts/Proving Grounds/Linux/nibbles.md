---
title: Nibbles
date: 2025-03-19
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Nibbles 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250319185357.png)

## Initial Access

Searching, we find [https://github.com/squid22/PostgreSQL_RCE](https://github.com/squid22/PostgreSQL_RCE).

Clone, create `venv` and install requirements.

Edit host and port and use port `80` on listener.

![](../assets/Pasted%20image%2020250319202545.png)

![](../assets/Pasted%20image%2020250319202553.png)

## Privilege Escalation

Get local flag.

![](../assets/Pasted%20image%2020250319202808.png)

`find` has SUID privs.

![](../assets/Pasted%20image%2020250319203721.png)

Looking in `gtfobins`.

![](../assets/Pasted%20image%2020250319203753.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250319203813.png)
