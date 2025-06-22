---
title: "Billyboss"
date: 2025-06-20
categories:
  - Proving Grounds
  - Windows
tags:
  - Proving Grounds
  - Windows
---


# Billyboss 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250410105310.png)

Port `80` has a `baget` instance.

![](../assets/Pasted%20image%2020250410105437.png)

Port `8081` has a `nexus repository manager`.

![](../assets/Pasted%20image%2020250410105647.png)

## Initial Access

Using `nexus:nexus`, we are in.

![](../assets/Pasted%20image%2020250410114808.png)
![](../assets/Pasted%20image%2020250410120640.png)

Now executing the exploit (and changing the IP and cmd inside).

![](../assets/Pasted%20image%2020250410120652.png)

Get the flag.

![](../assets/Pasted%20image%2020250410120741.png)

## Privilege Escalation

We have `SeImpersonatePrivilege` but I can't get potatos to work, `whoami` doesn't work, not valid for proof.

So we get all updates and notice one that is installed by `nathan`.

![](../assets/Pasted%20image%2020250410204028.png)
![](../assets/Pasted%20image%2020250410204156.png)

We can use this exploit: [https://github.com/danigargu/CVE-2020-0796](https://github.com/danigargu/CVE-2020-0796)

## Post Exploitation

![](../assets/Pasted%20image%2020250410135238.png)
