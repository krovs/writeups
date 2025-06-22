---
title: Clue
date: 2025-03-24
categories:
- Proving Grounds
- Linux
tags:
- Proving Grounds
- Linux
---

# Clue 🔺
<!-- more -->

## Enumeration

![](../assets/Pasted%20image%2020250324202019.png)

We can connect to `smb` shares.

![](../assets/Pasted%20image%2020250324203323.png)

The web server is forbidden.

![](../assets/Pasted%20image%2020250324203622.png)

Port `300` is for `Apache Cassandra`.

![](../assets/Pasted%20image%2020250324204153.png)

Searching for an exploit for `freeswitch`:

![](../assets/Pasted%20image%2020250324231900.png)

But it doesn't seem to work.

![](../assets/Pasted%20image%2020250324231916.png)

The exploit is using the default password `ClueCon`.

![](../assets/Pasted%20image%2020250324231938.png)

So the default password is not set.

Looking in the `smb` share `freeswitch`, we find `ClueCon`.

![](../assets/Pasted%20image%2020250324232501.png)

So the password is set in `/etc/freeswitch/autoload_configs/event_socket.conf.xml`.

Searching for an exploit for `cassandra`:

![](../assets/Pasted%20image%2020250324232218.png)

We can read files, so we can try to get the password from before.

![](../assets/Pasted%20image%2020250324232542.png)

And the password is different: `StrongClueConEight021`.

Using the exploit from before, we can change the password.

![](../assets/Pasted%20image%2020250324232817.png)

We can set a reverse shell.

![](../assets/Pasted%20image%2020250325001203.png)

## Privilege Escalation

`ps auxww` shows a `ruby` process with the `cassie` password:

![](../assets/Pasted%20image%2020250325005614.png)

`cassie:SecondBiteTheApple330`

![](../assets/Pasted%20image%2020250325005857.png)

With `sudo -l`, we see that we can execute `cassandra-web` as root, so:

![](../assets/Pasted%20image%2020250325013650.png)

Now, using the same exploit as before for reading files, we would be reading files as root.

Start a `cassandra-web` on another port and execute the script locally.

![](../assets/Pasted%20image%2020250325104449.png)

The script is only making a `curl` request with eight `../`, so we can do it without the script locally.

![](../assets/Pasted%20image%2020250325104528.png)

If we check Anthony's stuff, in bash history we see:

![](../assets/Pasted%20image%2020250325111457.png)

So the private key is the same for `anthony` and `root`, so read `id_rsa` and login via SSH.

![](../assets/Pasted%20image%2020250325111432.png)

## Post Exploitation

![](../assets/Pasted%20image%2020250325111529.png)
