---
title: Pebbles
date: 2025-03-18
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Pebbles 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250318232333.png)

Web page is...

![](../assets/Pasted%20image%2020250318233029.png)

And a `tomcat` at port `8080`.

![](../assets/Pasted%20image%2020250318234243.png)

With `feroxbuster` we found a `zm` folder that is a `zoneminder 1.29.0`.

![](../assets/Pasted%20image%2020250318234417.png)

Searching for vulnerabilities, we find...

![](../assets/Pasted%20image%2020250319000924.png)

There is a blind SQL vulnerability.

![](../assets/Pasted%20image%2020250319005238.png)

So we can put a PHP web shell.

![](../assets/Pasted%20image%2020250319005330.png)

And access port `3305`.

![](../assets/Pasted%20image%2020250319005417.png)

!!! bug

    Someone uploaded a reverse shell file and executed it but I can't get it to work.
