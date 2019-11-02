* The only version of main() with superpowers is the main() with this signature:

  ```
  public static void main(String[] args)
  ```

* If you do a static import for both the Integer class and the Long class, referring to MAX_VALUE will cause a compiler error, because both Integer and Long have a MAX_VALUE constant and Java won’t know which MAX_VALUE you’re referring to.

* ``` import java.*; ``` Will compile but not work. If want you define the ```ArrayList``` then you have to import the ``` import java.util.ArrayList;``` or ```import java.util.*;```

* A class can be declared with only public or default access; the other two access control levels don’t make sense for a class


### strictfp keyword

* [Good Read](https://www.geeksforgeeks.org/strictfp-keyword-java/)
* strictfp modifier is used with classes, interfaces and methods only.
  ``` strictfp class Test
  {   
      // all concrete methods here are
      // implicitly strictfp.    
  }
  strictfp interface Test
  {   
      // all  methods here becomes implicitly 
      // strictfp when used during inheritance.    
  }
  class Car
  {  
      // strictfp applied on a concrete method 
      strictfp void calculateSpeed(){}
  }  ```
* When a class or an interface is declared with strictfp modifier, then all methods declared in the class/interface, and all nested types declared in the class, are implicitly strictfp.
* strictfp cannot be used with abstract methods. However, it can be used with abstract classes/interfaces.
* Since methods of an interface are implicitly abstract, strictfp cannot be used with any method inside an interface.
  ```strictfp interface Test 
  {
      double sum();
      strictfp double mul(); // compile-time error here
  }
  ```
  
