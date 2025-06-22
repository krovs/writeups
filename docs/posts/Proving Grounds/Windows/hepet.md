---
title: Hepet
date: 2025-04-21
categories:
- Proving Grounds
- Windows
tags:
- Proving Grounds
- Windows
---


# Hepet 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250421205925.png)

`ftp` has anonymous access.

![](../assets/Pasted%20image%2020250421211418.png)

The webpage shows some users; a description is odd.

![](../assets/Pasted%20image%2020250421232636.png)

We can try to read messages with `pop3`.

![](../assets/Pasted%20image%2020250421232707.png)
![](../assets/Pasted%20image%2020250421233102.png)

## Initial Access

So we can send a malicious OpenOffice document as `mailadmin`. We can use [https://github.com/0bfxgh0st/MMG-LO.git](https://github.com/0bfxgh0st/MMG-LO.git) to generate it and `sendEmail` to send it.

![](../assets/Pasted%20image%2020250422133800.png)
![](../assets/Pasted%20image%2020250422133819.png)

## Privilege Escalation

Transfer `winpeas`.

![](../assets/Pasted%20image%2020250422082415.png)
![](../assets/Pasted%20image%2020250422082639.png)

We can hijack the binary.

![](../assets/Pasted%20image%2020250422135740.png)
![](../assets/Pasted%20image%2020250422135732.png)

Restarting the service doesn't work, so restart the machine.

![](../assets/Pasted%20image%2020250422135818.png)
![](../assets/Pasted%20image%2020250422135824.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250422135848.png)
