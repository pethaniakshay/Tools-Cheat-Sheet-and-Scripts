* The only version of main() with superpowers is the main() with this signature:

  ```
  public static void main(String[] args)
  ```

* If you do a static import for both the Integer class and the Long class, referring to MAX_VALUE will cause a compiler error, because both Integer and Long have a MAX_VALUE constant and Java won’t know which MAX_VALUE you’re referring to.

* ``` import java.*; ``` Will compile but not work. If want you define the ```ArrayList``` then you have to import the ``` import java.util.ArrayList;``` or ```import java.util.*;```
