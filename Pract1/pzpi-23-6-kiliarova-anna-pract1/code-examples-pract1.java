interface Product {
      void use();
      }

  class ConcreteProductA implements Product {
      public void use() {
          System.out.println("Product A");
      }
  }

  class ConcreteProductB implements Product {
      public void use() {
          System.out.println("Product B");
      }
  }
  abstract class Creator {
     abstract Product factoryMethod();

     void someOperation() {
         Product product = factoryMethod();
         product.use();
     }
 }

class ConcreteCreatorA extends Creator {
     Product factoryMethod() {
         return new ConcreteProductA();
     }
 }

class ConcreteCreatorB extends Creator {
     Product factoryMethod() {
         return new ConcreteProductB();
     }
 }

public class Main {
     public static void main(String[] args) {
         Creator creator = new ConcreteCreatorA();
         creator.someOperation();
     }
 }