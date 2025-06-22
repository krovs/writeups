---
title: Hunit
date: 2025-04-01
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Hunit 🔸
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250401101217.png)

We have a blog at port `8080`.

![](../assets/Pasted%20image%2020250401101347.png)

At port `1830` there is a game.

![](../assets/Pasted%20image%2020250401102311.png)

In a post source code of port `8080` we see...

![](../assets/Pasted%20image%2020250401121435.png)

Now with `feroxbuster` we can fuzz.

![](../assets/Pasted%20image%2020250401121458.png)

The one that works is `/api/?`:

![](../assets/Pasted%20image%2020250401121531.png)

![](../assets/Pasted%20image%2020250401121548.png)

```json
[
  {
    "login": "rjackson",
    "password": "yYJcgYqszv4aGQ",
    "firstname": "Richard",
    "lastname": "Jackson",
    "description": "Editor",
    "id": 1
  },
  {
    "login": "jsanchez",
    "password": "d52cQ1BzyNQycg",
    "firstname": "Jennifer",
    "lastname": "Sanchez",
    "description": "Editor",
    "id": 3
  },
  {
    "login": "dademola",
    "password": "ExplainSlowQuest110",
    "firstname": "Derik",
    "lastname": "Ademola",
    "description": "Admin",
    "id": 6
  },
  {
    "login": "jwinters",
    "password": "KTuGcSW6Zxwd0Q",
    "firstname": "Julie",
    "lastname": "Winters",
    "description": "Editor",
    "id": 7
  },
  {
    "login": "jvargas",
    "password": "OuQ96hcgiM5o9w",
    "firstname": "James",
    "lastname": "Vargas",
    "description": "Editor",
    "id": 10
  }
]
```

## Initial Access

`ssh` with the admin from before and...

![](../assets/Pasted%20image%2020250401131614.png)

Get the flag.

![](../assets/Pasted%20image%2020250401131645.png)

## Privilege Escalation

Transfer `linpeas` and found...

![](../assets/Pasted%20image%2020250401132825.png)

![](../assets/Pasted%20image%2020250401133013.png)

![](../assets/Pasted%20image%2020250401140144.png)

We can pivot to user `git` using the private key but we don't have commands.

![](../assets/Pasted%20image%2020250401133726.png)

With the private key, we can execute `git` commands like clone the server repo.

![](../assets/Pasted%20image%2020250401175945.png)

![](../assets/Pasted%20image%2020250401175959.png)

We can put a command in `backups.sh` that will be executed every 3 minutes.

![](../assets/Pasted%20image%2020250401191435.png)

![](../assets/Pasted%20image%2020250401191448.png)

Wait and check `/bin/bash`.

![](../assets/Pasted%20image%2020250401191626.png)

![](../assets/Pasted%20image%2020250401191721.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250401191747.png)
