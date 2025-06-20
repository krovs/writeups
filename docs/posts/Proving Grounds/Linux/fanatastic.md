---
title: "Fanatastic"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Fanatastic 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250404094543.png)

We have a `Prometheus` + `Grafana` stack.

![](../assets/Pasted%20image%2020250404094926.png)

## Initial Access

Searching for exploits, we have a path traversal one.

![](../assets/Pasted%20image%2020250404132329.png)

We can read the `grafana` database and get data source credentials from `/var/lib/grafana/grafana.db`.

![](../assets/Pasted%20image%2020250404132428.png)

![](../assets/Pasted%20image%2020250404132440.png)

Searching for an exploit to decrypt it, we have [https://github.com/Sic4rio/Grafana-Decryptor-for-CVE-2021-43798](https://github.com/Sic4rio/Grafana-Decryptor-for-CVE-2021-43798)

SSH with credentials.

![](../assets/Pasted%20image%2020250404132619.png)

## Privilege Escalation

The user belongs to the `disk` group, so we can read root files.

We can read the root private key and SSH to the host.

![](../assets/Pasted%20image%2020250404132907.png)

![](../assets/Pasted%20image%2020250404132921.png)

## Post Exploitation

Get the flags.

![](../assets/Pasted%20image%2020250404132938.png)
