---
title: Slort
date: 2025-04-18
categories:
- Proving Grounds
- Windows
tags:
- Proving Grounds
- Windows
---


# Slort 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250418172141.png)

Using `feroxbuster`, we discover a `/site` website.

![](../assets/Pasted%20image%2020250419011521.png)

## Initial Access

The URL has an RFI vulnerability, so we can call a reverse shell.

![](../assets/Pasted%20image%2020250419011558.png)

![](../assets/Pasted%20image%2020250419011617.png)

Get the flag.

![](../assets/Pasted%20image%2020250419011640.png)

## Privilege Escalation

There is a backup folder with `TFTP.EXE` inside and an `info.txt` that says that `tftp` will be executed every 5 minutes, and `rupert` can edit all. So generate a reverse shell and replace the binary, reboot the system, and wait 5 minutes.

![](../assets/Pasted%20image%2020250419015637.png)

![](../assets/Pasted%20image%2020250419015650.png)

![](../assets/Pasted%20image%2020250419015712.png)

![](../assets/Pasted%20image%2020250419015741.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250419015752.png)
