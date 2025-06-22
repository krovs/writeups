---
title: "Bratarina"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Bratarina 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250318203916.png)

Starting with `smb`, we have a `backups` folder and a file inside.

![](../assets/Pasted%20image%2020250318204555.png)

![](../assets/Pasted%20image%2020250318204623.png)

The web page shows:

![](../assets/Pasted%20image%2020250318204741.png)

Although `opensmtpd` is version `2.0.0`, we can use a `6.6.1` exploit.

![](../assets/Pasted%20image%2020250318214753.png)

## Initial Access

![](../assets/Pasted%20image%2020250318214839.png)

![](../assets/Pasted%20image%2020250318214851.png)

## Post Exploitation

![](../assets/Pasted%20image%2020250318214918.png)
