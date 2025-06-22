---
title: Scrutiny
date: 2025-04-19
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Scrutiny 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250419223352.png)

The web page is `onlyrands`, add to `/etc/hosts`.

![](../assets/Pasted%20image%2020250419223436.png)

![](../assets/Pasted%20image%2020250419223757.png)

At `/login` we have:

![](../assets/Pasted%20image%2020250419223824.png)

## Initial Access

Searching for an exploit, we have [https://github.com/Chocapikk/CVE-2024-27198](https://github.com/Chocapikk/CVE-2024-27198).

![](../assets/Pasted%20image%2020250419231522.png)

We can use that credential to access the UI and explore, and we find an `id_rsa` under the Marco Tillman project.

![](../assets/Pasted%20image%2020250420113828.png)

The key is protected, so using `ssh2john` and `john` we get `cheer` as password.

![](../assets/Pasted%20image%2020250420124502.png)

![](../assets/Pasted%20image%2020250420124517.png)

Get the flag.

![](../assets/Pasted%20image%2020250419234846.png)

## Privilege Escalation

This user has email, so let's check `/var/spool/email`.

![](../assets/Pasted%20image%2020250420124846.png)

We have the `matthew` password.

![](../assets/Pasted%20image%2020250420124948.png)

![](../assets/Pasted%20image%2020250420130046.png)

Pivot to `briand` and `sudo -l`.

![](../assets/Pasted%20image%2020250420130555.png)

Searching, we find [https://sploitus.com/exploit?id=EDB-ID:51674](https://sploitus.com/exploit?id=EDB-ID:51674), all `systemd` before `247` can be abused to gain root.

![](../assets/Pasted%20image%2020250420130930.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250420130939.png)
