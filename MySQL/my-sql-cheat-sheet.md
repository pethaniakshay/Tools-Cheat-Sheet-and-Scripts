##### Show current port of the my sql

```  SHOW GLOBAL VARIABLES LIKE 'PORT';  ```


##### Shutdown MySQL 

```  mysqladmin -u root -p shutdown  ```


##### Open mysql in console if it is running on other than the default port 3306

```  mysql -u root -P 3308 -p  ```


##### MySQL Version

```  SHOW VARIABLES LIKE "%version%"; ```
