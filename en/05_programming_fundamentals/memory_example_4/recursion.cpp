#include <stdlib.h>
#include <iostream>

// NOTE:
// the memory indicated in excel ignores all of the address pushing that's happening,
// as well as outputting the result of the function call.

// The example works with recursion,
// but if you understand how memory works,
// recursion as a concept should be trivial to understand.
// The use of recursion illustrates that the variables are bound to stack memory,
// rather than the function itself.

int recurse(int recursionLevel)
{
    int nextRecursionLevel = recursionLevel + 1;

    if (nextRecursionLevel < 3)
    {
        int result = recurse(nextRecursionLevel);
        result += 1;
        return result;
    }
    else
    {
        return 5;
    }
}

int main()
{
    int recursionLevel = 0;
    int result = recurse(recursionLevel);
    std::cout << result;

    // Note that at this point, the memory that's been used by recurse
    // has been reclaimed, that is, if you call recurse again, it will use the same memory slots.
    // So this does *exactly the same thing, on the exact same memory*.
    result = recurse(recursionLevel);
    return 0;
}

/* The operations done here, in order (approximately):

`main` setup:
- main() is called by the runtime.
- the memory for `recursionLevel` and `result` is reserved on the stack.
- the memory of `recursionLevel` is set to 0.

Setting up the function call of `recurse(0)`:
- the value of `recursionLevel` is put in a register.
- the address of the instruction `std::cout << result` is put on the stack.
- the processor jumps to the address of the first instruction of `recurse`.

`recurse(0)` function call:
- the value of `recursionLevel` is stored on the stack (note that this may be optimized out).
- memory for each local variable is allocated on the stack, 8 bytes.
- `nextRecursionLevel` is set to `recursionLevel + 1 = 1`.
- `nextRecursionLevel < 3` is evaluated to `true`.

Setting up the function call of `recurse(1)`:
- the value of `nextRecursionLevel` is put in a register.
- the address of `result += 1` is put on the stack.
- the processor jumps to the address of the first instruction of `recurse`.

`recurse(1)` function call:
- the value of `recursionLevel` is stored on the stack (note that this may be optimized out).
- memory for each local variable is allocated on the stack, 8 bytes.
- `nextRecursionLevel` is set to `recursionLevel + 1 = 2`.

Setting up the function call of `recurse(2)`:
- the value of `nextRecursionLevel` is put in a register.
- the address of `result += 1` is put on the stack. Let's say the memory address is 128 here.
- the processor jumps to the address of the first instruction of `recurse`.

`recurse(2)` function call:
- the value of `recursionLevel` is stored on the stack (note that this may be optimized out).
- memory for each local variable is allocated on the stack, 8 bytes.
- `nextRecursionLevel` is set to `recursionLevel + 1 = 3`.
- `nextRecursionLevel < 3` is evaluated to `false`, executing the instructions in the else branch.

Unrolling of the stack for `reverse(2)`:
- the processor puts 5 in a register.
- the processor unrolls the stack up until 128.
- the processor jumps to `result += 1` of `recurse(1)`
  (this address is stored in memory under address 128).

Finishing execution of `reverse(1)`:
- the processor copies the value of the register (5) into `result`.
- the processor adds 1 to `result`.
- the processor puts the value of `result` in a register.

Unrolling of the stack for `reverse(1)`:
- the processor unrolls the stack until the address of `result += 1` of `recurse(0)` on the stack.
- the processor jumps to `result += 1` of `recurse(0)`.

Finishing execution of `reverse(0)`:
- the processor copies the value of the register (6) into `result`.
- the processor adds 1 to `result`.
- the processor puts the value of `result` in a register.

Unrolling of the stack for `reverse(0)`:
- the processor unrolls the stack until the address of `std::cout << result` of `main` on the stack.
- the processor jumps to `std::cout << result` of `main`.

Finishing execution of `main`:
- the processor copies the value of the register (7) into `result`.
- the processor puts the value of `result` in a register.
- the processor calls `std::cout << result`.

*/
