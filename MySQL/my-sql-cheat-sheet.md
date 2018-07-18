##### Show current port of the my sql

```
SHOW GLOBAL VARIABLES LIKE 'PORT';
```


##### Shutdown MySQL 

```
mysqladmin -u root -p shutdown
```


##### Open mysql in console if it is running on other than the default port 3306

```
mysql -u root -P 3308 -p
```


##### MySQL Version

```
SHOW VARIABLES LIKE "%version%";
```


##### Initialize MySQL for first time

```
Note: First create folder named data in the mysql root directory

With Default password that can be fund from log file that will be located in data folder:
  mysqld --initialize

With no default password and username as root
  mysqld --initialize-insecure
  
With custom root username
  mysqld --initialize-insecure --user=akshay
  
  Note:  Add   --explicit_defaults_for_timestamp = 1   as argument if you get timestamp error.
```


##### MySQL Minimal ini file that have to be created while first time installtion in the root dir

```
[mysqld]

basedir = "/mysql-5.7.17"
datadir = "/mysql-5.7.17/data"
port = 3306
server_id = 1
log_error = "mysql_error.log"
pid_file = "mysql.pid"
socket = "/mysql-5.7.17/mysql.sock"

# Optional - Default Configuration
max_allowed_packet = 8M
key_buffer_size=16M

# Where do all the plugins live
plugin_dir = "/mysql-5.7.17/lib/plugin/"
```


##### Install / Remove MySQL as a windows service

```
Note: run window cmd as admin mode

mysqld --install-manual

mysqld --install

mysqld --remove
```

##### Create New Root Privilaged User

```
GRANT ALL PRIVILEGES ON *.* TO 'me'@'localhost' IDENTIFIED BY 'you';
```

##### Truncate all the table 

```
mysql -Nse 'show tables' DATABASE_NAME | while read table; do mysql -e "truncate table $table" DATABASE_NAME; done
```
```
mysql -Nse 'show tables' DATABASE -uMYUSER -pMYPASSWORD | while read table; do mysql -e "truncate table $table" DATABASE -uMYUSER -pMYPASSWORD ; done
```
