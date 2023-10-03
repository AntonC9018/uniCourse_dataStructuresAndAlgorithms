
void a()
{
    int i = 5;
    i = i + 5;
    // return;
}
/*
- Allocate space for `i` on the stack.
- Write 5 to `i`.
- Add 5 to `i`.
- Return (to address of `return;` stored by b).
*/

void b()
{
    a();
    return;
}

/*
- Allocate space for the next instruction on the stack.
- Save address of `return;` on the stack.
- Jump to first instruction of `a`.
- Return (to address of `return 0;` in main).
*/

int main()
{
    b();
    return 0;
}

/*
- Allocate space for the next instruction on the stack.
- Save address of `return 0;` on the stack.
- Just to first instruction of b.
- return 0;
*/