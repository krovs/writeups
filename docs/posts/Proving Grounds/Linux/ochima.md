---
title: "Ochima"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Ochima 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250419161210.png)

![](../assets/Pasted%20image%2020250419163225.png)

## Initial Access

[https://github.com/spookier/Maltrail-v0.53-Exploit/blob/main/exploit.py](https://github.com/spookier/Maltrail-v0.53-Exploit/blob/main/exploit.py)

![](../assets/Pasted%20image%2020250419163259.png)

![](../assets/Pasted%20image%2020250419163310.png)

## Privilege Escalation

![](../assets/Pasted%20image%2020250419163327.png)

We notice an `etc_Backup.sh` that is being executed as `root`.

![](../assets/Pasted%20image%2020250419163210.png)

![](../assets/Pasted%20image%2020250419163528.png)

So add a `nc` to us and wait.

![](../assets/Pasted%20image%2020250419164518.png)

![](../assets/Pasted%20image%2020250419164653.png)

![](../assets/Pasted%20image%2020250419165045.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250419165033.png)
