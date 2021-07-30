# Debian/Ubuntu Linux specific commands to Start/Stop/Restart Apache

**Restart/stop/start Apache 2 wen server**:

```
# /etc/init.d/apache2 restart/stop/start
```

Or

```
$ sudo /etc/init.d/apache2 restart/stop/start
```

or

```
$ sudo service apache2 restart/stop/start
```

## A note about Debian/Ubuntu Linux systemd users 

Use the following systemctl command on Debian Linux version 8.x+ or Ubuntu Linux version Ubuntu 15.04+ or above:

```
## Start command ##
systemctl start apache2.service
## Stop command ##
systemctl stop apache2.service
## Restart command ##
systemctl restart apache2.service
```

We can view status using the following command:

```
$ sudo systemctl status apache2.service
```

**Generic method to start/stop/restart Apache on a Linux/Unix**

The syntax is as follows (must be run as root user):

```
## stop it ##
apachectl -k stop
## restart it ##
apachectl -k restart
## graceful restart it ##
apachectl -k graceful
## Start it ##
apachectl -f /path/to/your/httpd.conf
apachectl -f /usr/local/apache2/conf/httpd.conf
```

See more [here](https://www.cyberciti.biz/faq/star-stop-restart-apache2-webserver/)
