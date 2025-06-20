---
title: "Hutch"
date: 2025-06-20
categories:
  - Proving Grounds
  - Active Directory
tags:
  - Proving Grounds
  - Active Directory
---

# Hutch 🔸
<!-- more -->


## Enumeration

![](../assets/Pasted%20image%2020250428202607.png)

Enumerating `LDAP` anonymously.

![](../assets/Pasted%20image%2020250428234112.png)

There is a user with a password in comment.

![](../assets/Pasted%20image%2020250428234222.png)

`fmcsorley:CrabSharkJellyfish192`

Use `bloodhound-python` to scout the domain.

![](../assets/Pasted%20image%2020250428235315.png)
![](../assets/Pasted%20image%2020250429002926.png)
![](../assets/Pasted%20image%2020250429002942.png)

This user can read the local admin password using `pylaps`.

![](../assets/Pasted%20image%2020250429003013.png)

So `Administrator:rD{7eI/@x9tG/[`

## Initial Access

Using `evil-winrm`.

![](../assets/Pasted%20image%2020250429003133.png)

## Post Exploitation

Get the flags.

![](../assets/Pasted%20image%2020250429003224.png)
![](../assets/Pasted%20image%2020250429003314.png)
