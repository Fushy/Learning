# Common

+ REPL read-evaluation-print loop \
    Is a simple interactive programming environment that takes user inputs, executes them, and returns the result.



# Code

+ Variables \
    Is a name that refers to a value that always represents a type 

- Expression \
    Combination of values and operators that produces a value

+ While statement \
    Tests the conditional expression that immediately follows.
    While the condition is considered as true, the body of the while statement is executed.
    When the condition is retested False, it goes out the while

- Primitives Type \
    Basics data structures unmodifiable. Building datas blocks for objects manipulation

+ Overloading \
    ...

# Operator

+ Modulo \
    Operator that return the remainder of the division:\
    10 / 3 = 3.333
    10 // 3 = 3
    10 % 3 = 1
    10 = 3 * 3 + 1
    x % y = x – (x // y) * y
 
- Logical Operators
  Perform Boolean logic on values

- Bitwise Operators \
    Allows manipulating individual bits of data at the most granular level\
    Same as Logical Operators but on a bit level
    Allows implementing optimise algorithms such compression/encryption algorithms\
    Often used to improve the speed of certain mathematical operations, it's way faster than usual operators
    Today, compilers and interpreters are quite capable of optimizing your code behind the scenes.
    + Signed Right Shift / Arithmetic Right Shift\
      It moves the binary sequence without the sign bit, and fills the resulting gap on the left with whatever the sign bit was\
      Lose the sign number\
      Always produce a non-negative integer
    + Unsigned Right Shift / Logical Right Shift / Zero-Fill Right Shift\
      It moves the binary sequence, including the sign bit, and fills the resulting gap on the left with zeros\
      Lose the sign number\
      Always produce a non-negative integer

# Encoding

## Binary System
Number representation system use by all informatics devices\
Two digits available: 0 & 1\
It requires more storage space than the decimal system but is much less complicated to implement in hardware\
Is perfect for electronic devices, which translate digits into different voltage levels\

+ Bit \
    A digit from the binary system

- Byte / Octet  \
    Contain 8 bit\
    The smallest unit of information in modern computing\
    Can represent 256 distinct values

+ Bit-Length \
    Number of binary digits from a value

- Bitmask \
    Used to let you isolate the bits wanted to apply some function on them selectively
    + x & 0xFF: output the 2 first byte
    + 1 & (x >> 5): output the bit in the 5th position
    + x & (1 << 5): put to 0 all bits except for the one that you’re interested in

+ Least-Significant Bit/Byte \
    + The bit/byte positioned at the rightmost place

- Most-Significant Bit/Byte \
    + The bit/byte positioned at the leftmost place
    + On signed integer, plays the role of a sign bit

+ Signed Integer\
  A binary representation of integer values that is defined by a sign bit on the most significant bit and a magnitude that's the rest
  Signed integers only make sense on fixed-length bit sequences\
  Have some issues
    + Two ways to represent zero
    + Adding two numbers with the same magnitude but opposite signs won’t make them cancel out
    + The carryover bit can sometimes propagate from magnitude to the sign bit, inverting the sign and yielding an unexpected result

- Magnitude\
  On a signed representation, that's all bits that is not the sign bit\
  The range of available values is symmetrical

+ Unsigned Integer\
    More suitable when you know for sure that you’ll never need to deal with negative numbers

## Standards

### One's complement representation\
  An evolved signed representation that solve its issues\
  Negative numbers are obtained by flipping the positive number’s bits using a bitwise NOT
  The range of available values is symmetrical
  Can add two numbers more reliably
+ Have some issues
    + Two ways to represent zero

### Two's complement representation\
  An evolved one's complement representation that solve its issues\
  Modern computers use this complement to represent integers\
  Add one to the result after using one's complement representation\
  Eliminate the minus zero, the old minus zero is the biggest negative value\
  There is as much positive as negative\
  The range of available values in two’s complement becomes asymmetrical

### IEEE 754 standard\
+ The most used standard for representing floating-point numbers\
Based of sign, exponent & bias, and mantissa bits\
float value = -1\*\*sign * 2\*\*(exponent-bias) * (mantissa + 1)\
+ Sign is the most significant bit
+ Exponent\
Stored as an unsigned integer\
You need to subtract the bias to the exponent it to recover the actual exponent\
+ Mantissa\
  Represent a fraction, their positional bit are powered by a negative value

### ASCII Standard
    ...

### UTF-8 Standard
+ UTF-8 is a superset of ASCII\
+ The letters u, r, and o occupy one byte each\
+ Euro symbol takes three bytes

## Byte Order (Endianness) \
   There’s no dispute about the order of bits in a single byte, while byte blocks can be read from left to right or from right to left.\
   Computers see bytes in a binary stream like humans see words in a sentence.
   Different computer architectures use different approaches, which makes transferring data between them challenging.\
   How to interpret 000000000000000000000111101100010 ?\
   + Big-Endian: Some find it natural to start from the left end because that’s how they read\
   + Little-Endian: While others prefer starting at the right end\
   + Major network protocols use the Big-Endian\
   + bitmap format always use Little-Enfian
   + Windows calculator representation tool use Big-Endian

### Big-Endian
Blocks added left to right\
The most-significant byte is the leftmost byte
00000000 00000000 00000111 10110001 0...\
00 00 07 B1...

### Little-Endian
Blocks added right to left\
The least-significant byte is the rightmost byte
+ ...0 00000000 00000000 00001111 01100010:\
62 0F 00 00...