# Top 50+ C# Interview Questions & Answers

> Source: [SimplyLearn - C# Interview Questions and Answers](https://www.youtube.com/watch?v=1u5E_GiXF9M)

---

## 📌 Top 5 Coding-Based Interview Questions

1. Write a program in C# to reverse a string
2. Write a program in C# to find if a given string is a palindrome or not
3. Write a C# program to find the substring from a given string
4. Write a C# program to find if a positive integer is prime or not
5. Write a singleton design pattern and how to implement it in C#

---

## 🟢 Beginner Level (Questions 1–24)

### Q1. How does C differ from C#?

| C | C# |
|---|---|
| Procedural programming | Object-oriented programming |
| Supports pointers | Pointers only in unsafe mode |
| No garbage collection | Garbage collection via CLR |
| Cross-platform | Requires .NET framework |
| Low-level abstraction | High-level abstraction |
| Used in commercial industries & engineering | Used for software development & network-related goals |

### Q2. What is an object and a class in C#?

- **Class** — a collection of properties and methods used to represent a real-time entity. It is a data structure that groups all instances into a single unit.
- **Object** — an instance of a class. Technically, a block of memory that can be stored as variables, arrays, or collections.
- **Example:** `Car` is a class; `Ford` and `Toyota` are objects (car manufacturers).

### Q3. What are the fundamentals of object-oriented programming?

The four pillars of OOP in C#:

1. **Encapsulation** — an object's internal representation is hidden from outside; only necessary information is accessible.
2. **Abstraction** — the process of identifying and eliminating irrelevant details from an object's critical behavior and data.
3. **Inheritance** — the ability to create new classes from existing ones by gaining access to, altering, and extending the behavior of parent class objects.
4. **Polymorphism** — "one name, many forms." Accomplished using several methods with the same name but different implementations.

### Q4. What is the Common Language Runtime (CLR)?

- CLR manages the execution of .NET programs.
- The just-in-time (JIT) compiler translates compiled code into machine instructions.
- CLR provides memory management, exception handling, type safety, and other services.

### Q5. What is managed and unmanaged code?

- **Managed Code** — executed by CLR. The .NET framework uses the garbage collector to clear unused memory.
- **Unmanaged Code** — any code executed by an application runtime in a framework other than .NET. The application runtime handles memory, security, and performance operations.

### Q6. What is an interface in C#?

- An interface is a class blueprint, similar to an abstract class.
- All methods declared within the interface are abstract.
- It cannot have a method body and cannot be instantiated.
- It can be used to achieve multiple inheritance.

### Q7. What are the different types of classes in C#?

1. **Partial Class** — members can be divided or shared across multiple files (keyword: `partial`).
2. **Abstract Class** — cannot be instantiated; must be inherited; must include at least one method (keyword: `abstract`).
3. **Sealed Class** — cannot be inherited; must create an object to access its members (keyword: `sealed`).
4. **Static Class** — does not allow inheritance; all members are also static (keyword: `static`).

### Q8. What is the difference between `==` operator and `.Equals()` method in C#?

- **`==` operator** — compares the identity of references.
- **`.Equals()` method** — compares the contents/values of strings.

### Q9. Explain code compilation in C#.

Three steps:
1. The C# compiler compiles source code into managed code and creates assemblies.
2. The CLR is loaded.
3. The CLR carries out the assembly.

### Q10. What are the differences between a class and a struct?

| Class | Struct |
|---|---|
| Can inherit | Cannot inherit |
| Passed by reference type | Passed by value type |
| Members are private by default | Members are public by default |
| Appropriate for large, complex operations | Appropriate for small, isolated models |
| Uses garbage collector for memory | Cannot use garbage collector |

### Q11. What is the difference between virtual method and abstract method?

- **Virtual Method** — has a default implementation; can optionally be overridden in derived class using the `override` keyword.
- **Abstract Method** — has no implementation; belongs to abstract class; derived class **must** implement it.

### Q12. Explain namespaces in C#.

- Namespaces organize large code projects.
- The most common namespace is `System`.
- We can create our own namespaces and use nested namespaces (one namespace inside another).
- Identified using the `namespace` keyword.

### Q13. What is the `using` statement?

- The `using` keyword indicates the program uses a specified namespace.
- **Example:** `using System;` — allows us to use `Console.WriteLine()` and `Console.ReadLine()` because `Console` is defined in the `System` namespace.

### Q14. Explain Abstraction.

- One of the OOP concepts.
- Displays only the essential features of a class and hides unnecessary information.
- **Example:** A car driver needs to know about steering, brakes, mirrors — but not the internal combustion engine or exhaust system.
- Hidden by declaring parameters as `private` using the `private` keyword.

### Q15. Explain Polymorphism.

- Means "same method, different implementations."
- Two types:
  - **Compile-time Polymorphism** (static binding / early binding / overloading)
  - **Runtime Polymorphism** (dynamic binding / late binding / overriding)
- **Example:** A man acts as a father, husband, and employee simultaneously.

### Q16. How is exception handling implemented in C#?

Using four keywords:
1. **try** — contains the block of code to be checked for exceptions.
2. **catch** — catches the exception with the help of an exception handler.
3. **finally** — runs regardless of whether an exception is thrown or not (used to close DB connections, I/O resources, etc.).
4. **throw** — throws an exception when a problem occurs.

### Q17. What are the C# input and output classes?

From the `System.IO` namespace:
| Class | Purpose |
|---|---|
| `FileStream` | Manipulation of files |
| `StreamWriter` | Writes characters to a stream |
| `StreamReader` | Reads characters from a stream |
| `StringWriter` | Writes to a string buffer |
| `StringReader` | Reads from a string buffer |
| `Path` | Operations on path information |

### Q18. What is StreamReader or StreamWriter class?

- Belongs to `System.IO` namespace.
- Used to read and write character data.
- **StreamReader members:** `Close()`, `Read()`, `ReadLine()`
- **StreamWriter members:** `Close()`, `Write()`, `WriteLine()`

### Q19. What is a destructor in C#?

- Used to clear memory and free resources.
- Handled automatically by the garbage collector (`System.GC.Collect()`).
- Can be implemented manually in some classes using the `~` (tilde) symbol.

### Q20. What is an abstract class?

- Denoted by the `abstract` keyword.
- Can only be used as a base class — must always be inherited.
- Cannot create an instance of the class itself.
- Methods have no implementations — must be implemented in child classes.
- All methods are implicitly `virtual`.

### Q21. What is the difference between boxing and unboxing?

- **Boxing** — converting a value type to a reference type (implicit).
- **Unboxing** — explicitly converting a reference type back to a value type.
- **Example:** `int val1 = 50;` → boxing converts `val1` to `object`; unboxing converts it back to `int`.

### Q22. What is the difference between `continue` and `break` statement?

- **`break`** — terminates the loop and exits it immediately.
- **`continue`** — skips only the current iteration and proceeds to the next.

### Q23. What is the difference between `final`, `finally`, and `finalize` blocks?

| Keyword | Description |
|---|---|
| `final` | Indicates a variable, method, or class is unchangeable |
| `finally` | Used with try/catch for exception handling; always executes regardless of exception |
| `finalize()` | Inherited from `java.lang.Object`; called by the garbage collector before removing an object from memory |

---

## 🟡 Intermediate Level (Questions 24–36)

### Q24. What exactly is an array?

- A data structure that stores multiple variables of the same data type.
- A set of variables stored in a single memory location.
- Supports single-dimensional (linear) and multi-dimensional (rectangular) arrays.

### Q25. What is a jagged array?

- An array of arrays — also known as a "jagged array."
- Can have a single dimension or multiple dimensions.
- Each row can have a different number of elements.

### Q26. Name some properties of arrays.

| Property | Description |
|---|---|
| `Length` | Returns the total number of elements |
| `Size` | Indicates whether the array's length is fixed |
| `ReadOnly` | Indicates whether the array is read-only |

### Q27. What is an Array class?

- Arrays can be created, manipulated, searched, and sorted using the `Array` class.
- Belongs to `System.Collections` namespace.
- Implements the `IList` interface — serves as the foundation for array-supporting language implementations.

### Q28. What exactly is a string? What are the properties of the String class?

- A string is a grouped character object.
- String variables can be declared in C#.
- **Properties:**
  - `Chars[i]` — returns the current string's character object at index `i`.
  - `Length` — returns the number of characters in the string.

### Q29. What is an escape sequence? Name some.

A backslash (`\`) indicates an escape sequence in C#. Common ones:
| Sequence | Meaning |
|---|---|
| `\n` | Newline character |
| `\b` | Backspace |
| `\\` | Backslash itself |
| `\t` | Tab |
| `\"` | Double quote |

### Q30. What are regular expressions? Search a string using regular expressions.

- A template that can match a set of input operators, constructs, and character literals.
- Used for string parsing and replacement.
- **Example:** `*` means "0 or more times before the preceding character" — so `a*b` matches `b`, `ab`, `aab`, `aaab`, etc.

### Q31. What are the fundamental string operations?

1. **Concatenate** — `string.Concat()` or the `+` operator.
2. **Modify** — `Replace(x, y)` replaces one string with another; `Trim()` cuts at beginning/end.
3. **Compare** — `string.Compare()` compares two strings (case-sensitive or not).
4. **Search** — `StartsWith()` and `EndsWith()` methods.

### Q32. What exactly is parsing? How do you parse a DateTime string?

- **Parsing** — converting a string into another data type.
- **Example:** Converting string `"100"` to `int` using `int.Parse()`.
- **DateTime example:** `DateTime.Parse("July 24, 2011")` converts a date string to a `DateTime` object.

---

## 🔴 Advanced Level (Questions 33–50+)

### Q33. What is a delegate? Explain.

- A delegate is a variable that holds a reference to a method.
- It is a function pointer or reference type.
- All delegates derive from `System.Delegate`.
- Both delegate and the technique it refers to can have the same signature.
- After declaring a delegate, an object must be created using the `new` keyword.
- Acts as an encapsulation for the reference method — called internally when the delegate is invoked.

### Q34. How to use delegates with events?

- Delegate authority is used to initiate and manage events.
- A delegate must always be declared first, followed by the events.
- A diagram shows three functions passed to the delegate to generate an event (event generator).

### Q35. What are events?

- User actions that cause the application to receive notifications it must respond to (e.g., mouse movements, key presses).
- A class that raises an event = **publisher**.
- A class that responds/receives the event = **subscriber**.
- If no subscriber exists, the event is never raised.
- Events are declared using delegates.

### Q36. What are the different types of delegates?

Three types:
1. **Single Delegate** — can only call one method.
2. **Multicast Delegate** — can call multiple methods; uses `+` and `-` operators for subscribe/unsubscribe.
3. **Generic Delegate** — no need for instance definition; classified into:
   - `Action` — replaces delegate definitions
   - `Func` — takes arguments and returns a result
   - `Predicate` — takes arguments and always returns `bool`

### Q37. What do multicast delegates mean?

- Holds references to multiple functions.
- When invoked, gathers all tasks the delegate refers to.
- All method signatures must be identical.

### Q38. What are synchronous and asynchronous operations?

- **Synchronous** — only one thread can access a resource at a time; waits for the method to complete before continuing.
- **Asynchronous** — method calls return immediately; program can perform other operations while the called method completes.
- In C#, achieved using `async` and `await` keywords.

### Q39. What exactly is reflection in C#?

- The ability of code to access an assembly's metadata during runtime.
- The program reflects itself and uses metadata to inform or change its behavior.
- `System.Reflection` namespace includes methods and classes for managing loaded types and techniques.
- Primarily used in Windows applications (e.g., viewing properties of a button in a Windows Form).

### Q40. What is a generic class?

- Also known as "generics."
- Creates classes or objects with no specific data type.
- The data type can be assigned at runtime.

### Q41. Explain get and set accessor properties.

- `get` — used to retrieve the value of a property.
- `set` — used to change the value of a property.
- Implements a mechanism for reading and writing the value of a private field.
- The `value` keyword denotes the value transferred to the property.

### Q42. What exactly is a thread? What is multi-threading?

- A **thread** is a collection of instructions that allows a program to perform concurrent processing.
- C# has a default thread; additional threads can be created to run code in parallel.
- **Multi-threading** = having different threads handle different processes.
- Thread methods: `Start`, `Sleep`, `Abort`, `Suspend`, `Resume`, `Join`.

### Q43. Name some properties of Thread class.

| Property | Description |
|---|---|
| `IsAlive` | True when the thread is active |
| `Name` | Returns (or sets) the thread's name |
| `Priority` | Returns the prioritized value set by the OS |
| `Background` | Gets/sets whether a thread is background or foreground |
| `ThreadState` | Describes the current thread state |

### Q44. What are the different states of a thread?

1. **Unstarted** — thread has been created
2. **Running** — thread begins execution
3. **Wait/Sleep/Join** — a thread called Sleep, Wait, or Join
4. **Suspended** — thread has been halted
5. **Aborted** — thread has died but not yet transitioned to Stopped
6. **Stopped** — thread has come to a halt

### Q45. What is a deadlock?

- Occurs when a process cannot complete its execution because two or more methods are awaiting the completion of another.
- Common in multi-threading scenarios.

### Q46. Explain lock, monitors, and mutex in multi-threading.

| Mechanism | Description |
|---|---|
| `lock` | Ensures only one thread can enter a specific code section at a time |
| `Monitor` | `Monitor.Enter()` and `Monitor.Exit()` internally implement a lock (lock is a shorthand for Monitor) |
| `Mutex` | Like lock but works across multiple processes; slower because of acquisition/release overhead |

### Q47. What is a race condition?

- Occurs when two threads access the same resource and attempt to change it simultaneously.
- Impossible to predict which thread will access the resource first.
- **Example:** Two threads `T1` and `T2` both try to write to shared resource `X` — only the last value written is saved.

### Q48. What is serialization and deserialization?

- **Serialization** — converting code to binary format for easy storage and retrieval.
- **Deserialization** — recovering C# code from binary form back to its original state.

### Q49. What are the different types of serialization?

1. **XML Serialization**
2. **SOAP Serialization**
3. **Binary Serialization**

### Q50. What is an XSD file?

- **XSD** = XML Schema Definition.
- Defines the structure of an XML file.
- Determines which elements should be represented in XML, in what order, and which properties should be present.
- During serialization, `xsd.exe` converts classes into XSD compiler form.

---

*Compiled from the SimplyLearn YouTube tutorial on C# Interview Questions.*
