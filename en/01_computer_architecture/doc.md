# General understanding of computer architecture

## Overview

On a conceptual level, a computer consists of a processor, 
which is able to execute a set of instructions, 
and memory, which can be used to store data.

Memory can be thought of as a linear tape of finite length where every slot has a number, also called an address.
Each slot of memory is typically represented by a byte, which will be explained a bit later.
For now, just think of a slot of memory as a small container for some data, like a number or a letter (also called a character).
A few of the first addresses are reserved by the operating system, 
so the first address that can be legally used by a program is off by some number, let's say 100.
Here's an example which conceptually represents some memory.

| Address | Data |
| ------- | ---- |
| 100     | A    |
| 101     | B    |
| 102     | 15   |
| 103     | 69   |
| 104     | 0    |

The processor can read memory from any address and can write data to any address.
It can perform operations with the data it reads from memory and write the result back to memory.


## Instructions, and a computer program example

For example, it could read the data at address 102 (which is 15), 
add the data at address 103 (which is 69) to it, and write the result (84) back to address 102.

Each of these operations is called an instruction. 
So a read from memory under an address is an instruction, 
adding the data from some other address to it is an instruction,
writing the result back to memory is an instruction.

> A clarification: 
> The processor has its own little pieces of memory, which it can do things with directly, 
> without loading them from the main memory.
> This special memory of the processor is usually pretty small, works pretty much the same way as the main memory.
> It is divided into a few "registers", which are just slots of memory at some concrete addresses.
> For example, the processor might have a register at address 0, which is called the "accumulator".
> When the processor reads from the main memory, it has to store the value into one of its registers.
> Now, this is not *exactly* what happens in a processor, it's a simplification, but it serves well as a conceptual model.

So the example three operations above could be rephrased as three instructions:
1. Read the data at address 102 of the main memory and store it in the first slot of memory in the processor (register).
2. Read the data at address 103 in the main memory and add it to the data in the first slot of memory in the processor.
3. Write the data in the first slot of memory in the processor to address 102 in the main memory.

Now, each of these instructions has an "identifier". 
An identifier is just a unique number, which can be used to uniquely identify an instruction.
In other words, if you know this identifier, you know exactly what instruction it refers to, be it read or write.

For sake of simplicity, let's say that the identifier for reading from main memory is 15,
adding a number in the main memory to a number in the processor memory is 22, and writing to main memory is 39.

So the three instructions above could be compacted as follows:
1. Use the instruction with identifier 15, where the first argument (main memory address) is 102 and the second argument (processor memory address) is 0. 
2. Use the instruction with identifier 22, where the first argument (processor memory address) is 0 and the second argument (main memory address) is 103.
3. Use the instruction with identifier 39, where the first argument (processor memory address) is 0 and the second argument (main memory address) is 102.

So each of these instructions takes two arguments, which in our case are addresses in the main memory and addresses in the processor memory.

To be clear, there may be another instruction, say 23, which also takes two arguments, 
but this time interprets them as two addresses in the processor memory, 
adding the values, and storing the result in the first address.
It does a bit of a different thing, which is why we gave it a separate unique identifier (number).

Another example: say, instruction 12, expects both the arguments to be addresses in the processor memory,
and it would copy the data from the second address to the first one.
It also deals with copying, but because we gave it a separate identifier, we can distinguish it from the other copying instruction 15.

So, we could rewrite the three instructions above as code now. Yes, this is how code that can be executed by the processor looks (conceptually, I argue you don't necessarily need to know the specifics):

```
15 102 0
22 0 103
39 0 102
```

Which the processor will see as just a sequence of numbers:

```
15 102 0 22 0 103 39 0 102
```

Here's how the processor would execute this code: it would read the first number as an instruction identifier (15).
It now looks at this identifier and realizes that it needs to interpret the following argument 
as a main memory address (102), and the one after that as a register (0).
So it reads 102 and it reads 0, and then it executes the instruction with identifier 15,
which will execute a predefined function in the processor, which will do what the instruction is meant to do.
Having done that, the processor will go on reading the program code, reading the instruction 22, realizing that it needs to interpret the next two numbers as register (0) and memory address (103), 
and then it would execute a predefined hardware operation that adds the two, storing the result in the register 0.

That's basically how computers can execute code at a high level (in other words, conceptually).


## What are the slots (bytes) in memory?

Each byte is just a block of 8 bits. Each bit can be in two distinct states, usually called 0 and 1.
But how is it that a byte can store numbers, letters, or any data for that matter? How does that work?

To understand this we need to understand number systems.

### Number systems

A number system can be used to represent any number.
Think of it as an abstract representation of quantity rather than a regular number you write down.
Now this leap of abstraction is very important in order to understand how number systems work.

Each number system has a base, which is the number of symbols it uses to represent numbers.
In the usual base 10 system, we use 10 symbols: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9.
Now let's say the base 3 number system would use the symbols 0, 1, 2.
But we can be more abstract and use any symbols we like to define a custom number system, 
as long as it follows the structure of one (described gradually in continuation). 
For example, instead of the symbols 0, 1 and 2 we could use x, y and z.
It's totally allowed as long as it works the same.
> What I need you to understand, is that the symbols 0-9 are not the only symbols that can be used to represent numbers.

Consequently, the base is also the amount of numbers one can represent with a single digit.
In the base 10 system, we can represent 10 numbers with a single digit: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9.
In base 3, it would be the 3 numbers 0, 1, 2.
In our custom base 3 system with the symbols x, y, z, it would be the 3 numbers,
written x, y and z, representing the numbers (abstract quantities) of 0, 1 and 2.

Where it gets interesting is when we introduce the concept of multiple digits used to make up a single number.
Let's say we're allowed to use 2 separate digits to represent a number. 
A natural choice which typical number systems obey is that we use the last digit to represent the amount of ones,
while the first digit represents the amount of base.
The explanation for this is that the numbers "loop around" and "carry over" when they do.
So, here are some two digit number written in base 3, and their value (abstract quantity) written in base 10.
Note that we increment (increase by 1) the number at each row, in both columns.

| Base 3 | Base 10 |
| ------ | ------- |
| 00     | 0       |
| 01     | 1       |
| 02     | 2       |
| 10     | 3       |
| 11     | 4       |
| 12     | 5       |
| 20     | 6       |
| 21     | 7       |
| 22     | 8       |

So when the second number reaches the maximum allowed number in the given base, which is 2 in this case,
it "carries over a 1" to the first digit, and the second digit resets to 0.
So we count 3 each time it loops around, which means the first digit increases by 1 for each 3 we have counted.
If you think about this, it means that the first digit represents the amount of 3s in the number.

In general, for any base N, this maximum number after which a "loop around" happens is N-1,
and the digit to the left counts the number of Ns.

Let's do another example, in our custom base with the letters x, y and z for the values 0, 1 and 2.

| Base xyz | Base 10 |
| -------- | ------- |
| xx       | 0       |
| xy       | 1       |
| xz       | 2       |
| yx       | 3       |
| yy       | 4       |
| yz       | 5       |
| zx       | 6       |
| zy       | 7       |
| zz       | 8       |

Just think about this a little bit until it clicks.

Now, the same thing happens in our usual base 10:
- Each digit can take on 10 different values, from 0 to 9.
- The first digit represents the amount of 10s in the number.
- The second digit represents the amount of 1s in the number.


Now what about 3-digit numbers? Well, again, just think about it: the second digit to the right will experience the same
"loop over" that happes at the last digit, in which case we'd carry over a 1 to the next digit to the left.
Hence, in case of base 3, the first digit will now count the number of times the digit to the right of it had looped over,
and since it loops over once every three threes that we count, it will count the number of 9s in the number.
Let's draw up another table:

| Base 3 | Base 10 |
| ------ | ------- |
| 000    | 0       |
| 001    | 1       |
| 002    | 2       |
| 010    | 3       |
| 011    | 4       |
| 012    | 5       |
| 020    | 6       |
| 021    | 7       |
| 022    | 8       |
| 100    | 9       |
| 101    | 10      |
| 102    | 11      |
| 110    | 12      |
| 111    | 13      |
| 112    | 14      |
| 120    | 15      |
| 121    | 16      |
| 122    | 17      |
| 200    | 18      |
| 201    | 19      |
| 202    | 20      |
| 210    | 21      |
| 211    | 22      |
| 212    | 23      |
| 220    | 24      |
| 221    | 25      |
| 222    | 26      |

You can see how the last number changes every time, 
the second one changes every 3 times we increment (increase by 1) the number, and the first one changes every 9 times.

So, in general, for a number system with base N, the Nth position from the right, represents the amount of $N^{M-1}$ in the number, where M is the position of the digit from the right.
For example, a number 1234 in base ten has:
- $` 4 * 10^0 = 4 `$ ones,
- $` 3 * 10^1 = 3 `$ tens,
- $` 2 * 10^2 = 2 `$ hundreds,
- $` 1 * 10^3 = 1 `$ thousand.

And to get the final number, you just have to add these quantities together.

The number 3321 in base 4 would be:
- $` 1 * 4^0 = 1 `$ ones,
- $` 2 * 4^1 = 2 `$ fours,
- $` 3 * 4^2 = 3 `$ sixteens,
- $` 3 * 4^3 = 3 `$ sixty-fours.

Again, here I wrote the numbers in base 10, but think what would happen if I wrote them in base 4?
Here it is:
- $` 1 * 10^0 = 1 `$ ones,
- $` 2 * 10^1 = 2 `$ "one zeros",
- $` 3 * 10^2 = 3 `$ "one zero zeros",
- $` 3 * 10^3 = 3 `$ "one zero zero zeros".

If you're confused why 4 just became 10, that's because the number of symbols of any base N, 
written in that number base N, will look like 10.
In this case we wrote 4 in base 4, which makes it 10 (we read it as "one zero" or "one oh", not as "ten").
Reread the examples above if you're confused.

Sometimes you'll see numbers in different bases written with a subscript of the base, written in the usual base 10.
For example 3321<sub>4</sub> means 3321 represents a number in base 4.

To convert a number from base N to base M... You just write the powers of each digit in base M, 
and then just add them up in that base. It should make perfect sense if you think about it.

Let's convert from 3321<sub>4</sub> to base 10: $1 * 4^0 + 2 * 4^1 + 3 * 4^2 + 3 * 4^3 = 1 + 8 + 48 + 192 = 249$

And now another example 2101<sub>3</sub> from base 3 to base 5.
(you add and multiply the same way as in base 10, just that you have to carry over when you reach the base):
- $1 * 3^0 = 1 * 1_{10}$
- $0 * 3^1 = 0 * 3_{10}$
- $1 * 3^2 = 1 * 9_{10}$
- $2 * 3^3 = 2 * 27_{10}$

Now we can write 1, 3, 9 and 27 in base 5. 
- $1_{10} = 1_{5}$
- $3_{10} = 3_{5}$
- $9_{10} = 1 * 5^1 + 4 * 5^0 = 14_{5}$
- $27_{10} = 1 * 5^2 + 0 * 5^1 + 2 * 5^0 = 102_{5}$

Now we can replace the coefficients in the base 10 written initially with the coefficients in base 5:
- $1 * 1_{10} = 1 * 1_{5} = 1_{5}$
- $0 * 3_{10} = 0 * 3_{5} = 0_{5}$
- $1 * 9_{10} = 1 * 14_{5} = 14_{5}$
- $2 * 27_{10} = 2 * 102_{5} = 204_{5}$

Now we just add them up to get the result in base 5: $1_5 + 0_5 + 14_5 + 204_5 = ...$
Here we can do the addition just like regular, using a table 
(we just have to carry over when we reach 5, instead of the regular 10):
```
204 +
 14 +
  0 +
  1 =
----
224
```

Let's do another one: 1234<sub>10</sub> from base 10 to base 2: 

### How does this relate to bytes?

Now the base 2 (binary) is special for computers, because it uses two symbols for each digit: 0 and 1.
Now remember, we can use any symbol we want to represent these, so we will use the states of bits in memory for this.
Recall that each bit in memory can be in one of two distinct states.
To make memory analogous to binary numbers, we will call these states 0 and 1.
This is done in order to simplify the abstraction, to make it easier to find similarities between memory and binary numbers.

Now, it becomes obvious that we can store numbers in memory. 
> To understand how we store e.g. letters, you need to understand the concept of encoding, which will be discussed later.

What's the largest number we can store in a byte? 
Well, a byte is 8 bit (binary digit). 
And what's the largest number you can store in 8 digits?
Well, the one where all of the digits are equal to the largest symbol in the number system, N - 1, where N is the base.
In base 2 this means a number with all 1 for each of the 8 digits, which is 11111111<sub>2</sub>.
If we convert it to base 10, via the idea described above, we get 255<sub>10</sub>.

So each byte can store numbers in range 0-255<sub>10</sub>, inclusive.


### Additional resources

Processor architecture, simplified, but way more in depth than I have described here: [A (Very) Simplified CPU Diagram](https://www.youtube.com/watch?v=8VakkEFOiJc)