## Interface Segregation Principle (ISP):

- Interface segregation principle is used to define independent interfaces with their corresponding behaviors (methods), so that they can be used and extended independently.
- This makes interfaces (abstract classes) independent to use, and does not affect concrete classes when there is any change in interfaces
- Principles:
  - Clients (concrete classes/low level implementation of interfaces/abstract class) should not be forced to depend on interfaces they do not use
  - No code should be forced to depend on methods it does not use.

- Example:
  - Suppose there is a Shape class with get_area() method.
  - we can use that class as parent class for Square, Circle, Triangle
  - for a new 3d shape class if we want to calculate volume.
  - we should not extend Shape class - which would violate DIP -> Because all the other Shapes (Sqare, Circle, Triangle) also now have to calculate volume (which they cannot!)
  - Instead use a separate interface 3DShape which will have a get_volume() abstractmethod, and another interface 2DShape for 2d shapes.

Blog: https://stackify.com/interface-segregation-principle/

## Dependency Inversion principle (DIP):

- Dependency inversion principle is used make sure that the low level modules/classes do not depend on concrete implementation but on highlevel abstractions (interfaces/abstract classes)
- Principle:
  - High-level modules should not depend on low-level modules. Both should
    depend on Abstractions(interfaces)
  - The High-level modules should not import anything from low-level mudules.
    they both must use abstractions.
  - Abstractions should not depend on details. Details(concrete implementation)
    should depend on abstractions.

- Example:
  - Scenario:
    - A payment processing system needs to charge customers.
    - Initially, the system only supports credit card payments.
    - The `PaymentProcessor` class directly creates and uses `CreditCardPayment` to process payments.
    - This violates DIP because:
      - The high-level module (`PaymentProcessor`) depends on a low-level module (`CreditCardPayment`).
      - Adding new payment methods (UPI, PayPal, NetBanking) would require modifying `PaymentProcessor` each time.

  - How to apply DIP:
    - Create an abstract interface `PaymentMethod` with a method like `pay(amount)`.
    - Implement separate classes:
      - `CreditCardPayment`
      - `UPIPayment`
      - `PayPalPayment`
      - `NetBankingPayment`
    - `PaymentProcessor` should depend only on the abstraction (`PaymentMethod`), not the concrete implementations.
    - New payment methods can be added without changing `PaymentProcessor`.

Blog: https://stackify.com/dependency-inversion-principle/

## Decorator Pattern:

- Attach Additional responsibilities to an object dynamically.
- Decorators provide a flexible alternative to subclassing for extending functionality.
- wiki: design pattern that allows behavior to be added to an individual object, dynamically, without affecting the behavior of other instances of the same class.

Example:

- Scenario:
  - A system needs to represent different types of coffee and allow optional customizations.
  - Initially, only a basic coffee type exists with a fixed description and cost.
  - Adding new customizations (like milk, sugar, cream) by modifying the base class would cause code bloat and violate open–closed principles.
  - A flexible way is needed to combine multiple optional features without altering the existing component.

- How the Decorator Pattern is applied:
  - Define an abstract component that specifies the required behavior (cost and description).
  - Create a concrete base component that provides the simplest implementation.
  - Introduce a base decorator class that wraps another component while maintaining the same interface.
  - Implement concrete decorators where each adds a specific enhancement (e.g., extra cost and modified description).
  - Stack multiple decorators at runtime to build a final customized object.

- Summary:
  - The base object represents the core behavior.
  - Decorators extend behavior incrementally without modifying existing code.
  - Functionality is combined dynamically through wrapping rather than subclassing.
  - This allows scalable, flexible customization with minimal dependencies.

Blog: https://refactoring.guru/design-patterns/decorator
