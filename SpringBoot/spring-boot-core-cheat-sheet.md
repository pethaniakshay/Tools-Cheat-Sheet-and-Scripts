##### Pass the app port while starting app

Pass the following arg as command line args while executing jar or application class. [In Eclipse pass as the VM argument]
```
-Dserver.port=4125
```

##### Run specific profile and external config files

As Program arguments add following args:
```
java -jar application.jar --spring.profiles.active=prod --spring.config.location=c:\config

```

As VM arguments:
```
java -jar -Dspring.profiles.active=prod application.jar
```
