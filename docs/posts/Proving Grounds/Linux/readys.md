---
title: Readys
date: 2025-04-01
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Readys 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250401193030.png)

Website at port `80` is a `WordPress` site.

![](../assets/Pasted%20image%2020250401193558.png)

Using `wpscan`, we find a local file inclusion in the plugin.

![](../assets/Pasted%20image%2020250401195433.png)

![](../assets/Pasted%20image%2020250401195444.png)

So we have `alice` user.

We can see the `redis` config at `/etc/redis/redis.conf`.

![](../assets/Pasted%20image%2020250401203659.png)

So we have `alice` user and the `redis` password `Ready4Redis?`.

We can log in to `redis`.

![](../assets/Pasted%20image%2020250401204513.png)

## Initial Access

Searching for an RCE exploit:

[https://github.com/jas502n/Redis-RCE](https://github.com/jas502n/Redis-RCE)

![](../assets/Pasted%20image%2020250401213340.png)

## Privilege Escalation

Make another reverse shell for a more stable session.

![](../assets/Pasted%20image%2020250401214116.png)

![](../assets/Pasted%20image%2020250401214130.png)

`mysql` config:

![](../assets/Pasted%20image%2020250401214327.png)

![](../assets/Pasted%20image%2020250401214941.png)

`admin:$P$Ba5uoSB5xsqZ5GFIbBnOkXA0ahSJnb0`

Can't crack it.

Transfer `linpeas.sh`.

![](../assets/Pasted%20image%2020250401221345.png)

Using `pspy64`, we see it.

![](../assets/Pasted%20image%2020250401222650.png)

![](../assets/Pasted%20image%2020250401223022.png)

We can exploit the `tar` wildcard, but not with this user; we need `alice`.

Find a writable folder to put a PHP file and execute it like before with LFI and get a reverse shell.

![](../assets/Pasted%20image%2020250401235624.png)

![](../assets/Pasted%20image%2020250401235632.png)

![](../assets/Pasted%20image%2020250402000244.png)

![](../assets/Pasted%20image%2020250402000303.png)

![](../assets/Pasted%20image%2020250402000336.png)

## Post Exploitation

Get the flags.

![](../assets/Pasted%20image%2020250402000350.png)
