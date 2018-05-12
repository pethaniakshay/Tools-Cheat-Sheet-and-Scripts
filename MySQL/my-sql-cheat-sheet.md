##### Show current port of the my sql

```
SHOW GLOBAL VARIABLES LIKE 'PORT';
```


##### Shut down mysql 

```
mysqladmin -u root -p shutdown
```


##### open mysql in console if it is running on other than the default port 3306

````
mysql -u root -P 3308 -p
```