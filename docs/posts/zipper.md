---
title: "Zipper"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Zipper 🔺
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250419114322.png)

The web is an app that zips all files you upload.

![](../assets/Pasted%20image%2020250419114634.png)

## Initial Access

We can see an LFI by clicking on home, and using a PHP filter we can see PHP code.

![](../assets/Pasted%20image%2020250419135029.png)

![](../assets/Pasted%20image%2020250419135041.png)

The filter is removing the last extension.

We can upload a reverse shell to be zipped and then execute it by abusing zip slip without the extension.

![](../assets/Pasted%20image%2020250419135149.png)

![](../assets/Pasted%20image%2020250419135201.png)

![](../assets/Pasted%20image%2020250419135254.png)

Get the flag.

![](../assets/Pasted%20image%2020250419135310.png)

## Privilege Escalation

There is a backup script with logs in `/opt`, read the logs.

![](../assets/Pasted%20image%2020250419135336.png)

![](../assets/Pasted%20image%2020250419135346.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250419135359.png)
