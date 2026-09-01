# Lab 3

Topic: **How numbers are stored in bytes**.

[Companion video](https://www.youtube.com/watch?v=3HnvK8WrK4M&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=4)

## Questions

- Explain how to derive the maximum number that can be stored in one byte. What about two bytes?
- Why is this maximum number one less than the number of possible combinations of bits in those positions?
- Given a number `x` (for example, `0000 0011`), what must be done to obtain the representation of its negative
  (in the two's complement system)? Derive a formula/algorithm (`1111 1101`).
- Under what conditions does $`a + b < a`$ if both $`a`$ and $`b`$ are positive and represented using 8 bits?
- What digits are used in the hexadecimal system?
- How do you convert `0101 1111` to hexadecimal?
- In which other numeral systems can an 8-bit value be written without performing calculations?
  > <details>
  > <summary>hint</summary>
  >
  > A group of X bits corresponds to one digit in that system.
  > </details>
  >
  > <details>
  > <summary>hint 2</summary>
  >
  > In the hexadecimal numeral system, X = 4.
  > </details>
  >
  > <details>
  > <summary>hint 3</summary>
  >
  > Grouping the bits in pairs gives `01 01 11 11`.
  > Each of these values can be represented by a single digit in a numeral system
  > where the number of digits equals the number of values that can be represented by 2 bits.
  > Two bits can represent 4 values (`00`, `01`, `10`, `11`).
  > That is, we can use the base-4 system: `01 01 11 11 -> 1 1 3 3 -> 1133`.
  > </details>
  >
  > <details>
  > <summary>question</summary>
  >
  > Why must the system's base be a power of two?
  > </details>
