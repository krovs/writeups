---
title: "Exfiltrated"
date: 2025-06-20
categories:
  - Proving Grounds
  - Linux
tags:
  - Proving Grounds
  - Linux
---

# Exfiltrated 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250403225903.png)

Add `exfiltrated.offsec` to `/etc/hosts`.

The webserver shows a `Kickstart` page.

![](../assets/Pasted%20image%2020250403230105.png)

We can log in with `admin:admin`.

## Initial Access

[https://github.com/Swammers8/SubrionCMS-4.2.1-File-upload-RCE-auth-](https://github.com/Swammers8/SubrionCMS-4.2.1-File-upload-RCE-auth-)

![](../assets/Pasted%20image%2020250404002314.png)

## Privilege Escalation

Get a reverse shell.

![](../assets/Pasted%20image%2020250404003535.png)

![](../assets/Pasted%20image%2020250404003541.png)

There is a script using `exiftool` that is being executed every minute.

![](../assets/Pasted%20image%2020250404014546.png)

Following this guide, we can generate a malicious jpg: [https://ine.com/blog/exiftool-command-injection-cve-2021-22204-exploitation-and-prevention-strategies](https://ine.com/blog/exiftool-command-injection-cve-2021-22204-exploitation-and-prevention-strategies)

Transfer the jpg with the payload to the path of the script and set a listener.

![](../assets/Pasted%20image%2020250404014506.png)

![](../assets/Pasted%20image%2020250404014559.png)

## Post Exploitation

Get the flags.

![](../assets/Pasted%20image%2020250404014618.png)
