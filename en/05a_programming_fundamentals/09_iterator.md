# Iterators

An *iterator* is a powerful programming pattern that allows you to abstract the logic
of iterating over a collection of items.

## Iterator pattern example

Imagine you had a tree graph, and you wanted to do a 
[depth-first traversal of it](./iterator/graph_1.cpp), 
printing all of the values.

Now that's simple enough, but what if you also wanted 
to compute the sum of all values in the nodes?
You'll have to duplicate the traversal function, 
and just change the logic that you do:

```cpp
int sumDFS(const Node* node)
{
    int result = node->value;
    for (size_t i = 0; i < node->children.size(); i++)
        result += sumDFS(node->children[i]);
    return result;
}
```

You can see how this might become problematic if the traversal logic was more involved
than just recursively looping through the children.

Now, one of the ways to solve this would be to use the strategy pattern,
aka passing in a function to be executed when visiting a node.
How you do that will be described later.

Here, we will discuss the iterator pattern instead, 
which is another solution to this problem,
and to that a more flexible one.
It will allow you to pause the traversal, and resume it later, as well as do 
any operation with the elements, and accessing any of your variables you want.

The idea is to store the current state of iteration in an object,
effectively representing how the stack will look in the recursive traversal,
and then define functions to advance the iterator to the next element
(and possibly more functions to e.g. go to the previous one).
We will also need a way to signal that the iteration has ended.
See [the code](./iterator/graph_manual_iterator.cpp).

> I recommend you take some time with the debugger 
> to understand how the program works.

Sure, it is more complicated, especially the fact that in this case you have 
to imitate the stack manually (you don't always have to),
and it will generally turn out more complicated than straightforward iteration,
but the added flexibility + removing code duplication may be really valuable.

## C++ iterators

C++ has a "standard way" of doing iterators, which is required for some
templated functions in the standard library to work:

- The iterator type overloads the `++` operator, to mean the `advance` method from my example.
  It also optionally overloads the `--` operators, to go back to the previous element.

- The iterator type overloads the `*` operator, to mean the `value` method from my example. 
  `*` as in pointer dereference. It should return a reference if possible.

- The iterator has a special state that means the end of iteration.
  In my case, I defined an `empty` method, but we could represent this "empty" state
  with both vectors being empty.
  Emptiness is then checked by comparing the iterator against this special state.

- Types that define a single way of iterating may define a `begin` and `end` method,
  which return the iterator state of the first element, 
  and the special "empty" state respectively.

See [the same example as before, but using the standard iterator pattern](./iterator/graph_standard.cpp)

The motivation for a design like this is to mimic the interface that you have with pointers.
`++p` moves the pointer by one element, `*p` reads the value at the address,
and `p == start+count` checks if we've reached the end of an array, for example.

## Benefits of the stardard way

If you do your iterator the C++ way, you get some nice syntax for range iteration.
If your type has `begin` and `end` methods, you can use it in a range-based for loop.
See [an example](./iterator/graph_range_for.cpp).

This syntax is enabled for most container types, because they follow this pattern,
defining `begin` and `end` methods, as well as an iterator type with the operations
described above.

You don't have to define another type. 
If it only makes sense to do one kind of iteration for your data structure,
or some sort of way of iterating should obviously be the default,
you can define a `begin` and an `end` method for your container type directly.
That would make sense for e.g. a `DynamicArray`, but it probably won't for a graph.


# `static_cast`, `reinterpret_cast`, `bit_cast`

`static_cast` for basic types is equivalent to a regular C cast.
It's different only in the context of class inheritance.
It can cast, with potentially modifying the pointer,
to a less derived type, but not the other way.

`reinterpret_cast` is a cast that just changes the type of a pointer,
without changing the address, skipping checks if the conversion is valid.

`bit_cast` can be used to reinterpret the bits of a type as another type.
For example:
```cpp
float a = 5.0f; // 40 a0 00 00 = 5.0
int b = std::bit_cast<int>(a); // 40 a0 00 00 = 1084227584
int c = static_cast<int>(a); // 5
```

