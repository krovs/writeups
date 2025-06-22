---
title: Roquefort
date: 2025-04-08
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Roquefort 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250408174349.png)

## Initial Access

At port `3000` there is a `gitea` instance. We can create a user.

![](../assets/Pasted%20image%2020250408201550.png)

In the pre-receive hook, we can put a reverse shell.

![](../assets/Pasted%20image%2020250408201613.png)

![](../assets/Pasted%20image%2020250408201628.png)

Get the flag.

![](../assets/Pasted%20image%2020250408201642.png)

## Privilege Escalation

Transfer `linpeas`.

![](../assets/Pasted%20image%2020250408204613.png)

![](../assets/Pasted%20image%2020250408205130.png)

![](../assets/Pasted%20image%2020250408205245.png)

![](../assets/Pasted%20image%2020250408215231.png)

We can write to `/usr/local/bin` so we can create a `run-parts` file that will be executed as `root`.

![](../assets/Pasted%20image%2020250408215504.png)
![](../assets/Pasted%20image%2020250408215515.png)

We wait and...

![](../assets/Pasted%20image%2020250408215535.png)

![](../assets/Pasted%20image%2020250408215557.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250408215607.png)
