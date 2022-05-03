# Python's overview

## Zen of Python
+ Beautiful is better than ugly.
+ Explicit is better than implicit.
+ Simple is better than complex.
+ Complex is better than complicated.
+ Flat is better than nested.
+ Sparse is better than dense.
+ Readability counts.
+ Special cases aren't special enough to break the rules.
+ Although practicality beats purity.
+ Errors should never pass silently.
+ Unless explicitly silenced.
+ In the face of ambiguity, refuse the temptation to guess.
+ There should be one-- and preferably only one --obvious way to do it.
+ Although that way may not be obvious at first unless you're Dutch.
+ Now is better than never.
+ Although never is often better than *right* now.
+ If the implementation is hard to explain, it's a bad idea.
+ If the implementation is easy to explain, it may be a good idea.
+ Namespaces are one honking great idea -- let's do more of those!

## Definition

+ High level language
+ Is slow
+ Easy to read and to understand
+ One of the most used programming languages in the world
+ One of the biggest community contributors about projects/library in the world

## File

+ Python source files have .py or .pyw suffix
  + py  suffix for executing with a console
  + pyw suffix for executing without a console

+ Python clean source files
  + Are UTF-8-encoded text files
  + use #!/usr/bin/env python3 on the first line of a program to specify the interpreter
    + UNIX: give execute permissions to run the program by typing x.py into your shell.

## IDE

+ Two mainstream IDE
    + PyCharm
    + VisualStudio

## Code

### Syntax notable

+ Use # to comment code lines
+ Use 4 spaces instead of TAB
  + Uses alignment spaces to delimit blocks. Four spaces per indentation level.
+ It does not include postfix operators like the increment (i++) or decrement (i--) operators available in C.
+ It does not include Do While statement
+ It does not include the unsigned right shift operator
+ All numeric literals are case-insensitive

### Byte representation

+ Big-Endian order
+ There’s no sign bit at all
+ All integers are signed (all numbers have an implicit sign attached to them)
+ Integers are stored as if there were an infinite number of bits at your disposal
+ Follows a custom adaptive strategy that works like sign-magnitude with an unlimited number of bits
+ Use IEEE 754 standard to represent floating number

### Operators

#### Arithmetic

+ a + b
+ a - b
+ a * b
+ a / b
+ a // b
+ a % b
+ a ** b

#### Logical

+ Lazily from left to right
+ Return bool type
+ A Boolean expression takes the value of the last evaluated operand
+ Cannot be overloaded
+ Do not have XOR logical operator

+ a and b
+ a or b
+ not a


#### Bitwise

+ Not lazily
+ Designed primarily to work with integers
+ Return int type
+ Are often overloaded

+ a & b
+ a | b
+ a << b
+ a >> b
+ a ^ b

#### Assign

+ a += b
+ a -= b
+ a *= b
+ a /= b
+ a //= b
+ a %= b
+ a **= b
+ a &= b
+ a |= b
+ a <<= b
+ a >>= b
+ a ^= b

### Type

+ Strings \
  Are represented as arrays of Unicode code points (ordinal values).
