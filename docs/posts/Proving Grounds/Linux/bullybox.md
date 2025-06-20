---
title: "Bullybox"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Bullybox 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250402102107.png)

Add `bullybox.local` to `/etc/hosts`.

![](../assets/Pasted%20image%2020250402102204.png)

We find [`CVE-2022-3552`](https://github.com/0xk4b1r/CVE-2022-3552), but we need admin credentials.

Using `feroxbuster`, we can use `-x git` and get a `.git` repository.

Download with `git-dumper`:

![](../assets/Pasted%20image%2020250402113528.png)

![](../assets/Pasted%20image%2020250402113607.png)

## Initial Access

![](../assets/Pasted%20image%2020250402115444.png)

![](../assets/Pasted%20image%2020250402115455.png)

## Privilege Escalation

The user has `sudo` privileges with `ALL`, so:

![](../assets/Pasted%20image%2020250402115656.png)

## Post Exploitation

Get the flag:

![](../assets/Pasted%20image%2020250402115704.png)
