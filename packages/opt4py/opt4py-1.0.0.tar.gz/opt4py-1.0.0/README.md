# opt4py

Adds to Python an `Option` container class that handles seamlessly NoneType checks in a monadic way. Similar to `Option`
in Rust or `Optional` in Java, but it also overloads every operator for a smooth use without worries.

## Usage
```python
>>> from opt4py import Option
>>> Option(1)
Option(1)
>>> Option("Hello World!")
Option(Hello World!)
>>> Option()
Option(None)
>>> Option(1) + 1
Option(2)
>>> Option(2) * Option(2)
Option(4)
>>> Option(5).unwrap()
5
>>> Option(8).map(lambda x: x*2)
Option(16)
>>> Option(2) == 2
True
>>> Option(2) > 3
False
```