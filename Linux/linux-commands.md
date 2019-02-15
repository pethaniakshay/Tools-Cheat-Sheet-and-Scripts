##### journalctl see live log

```
journalctl -u xyz.service -f
```


##### make any user sudo user with no password permission

This will help to run sudo in shell script

```
sudo visudo -f /etc/sudoers

Enter the following line in the opened file:

jenkins ALL=(ALL) NOPASSWD: ALL

where jenkins is the user name
```
