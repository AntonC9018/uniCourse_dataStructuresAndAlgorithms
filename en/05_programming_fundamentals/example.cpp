#include <stdlib.h>
#include <iostream>

int main()
{
	// TODO: Show this memory on a picture, people don't understand it as comments.

	// 0 0 0 69
	int i = 69;
	// 0 0 0 5
	// 0 0 0 6
	// 0 0 0 0
	// 0 0 0 0
	// 0 0 0 0
	int arr[5] = { 0 };
	arr[0] = 5;
	arr[1] = 6;

	// 0 0 0 0 0 0 0 35 
	int* iPointer = &i; // make sure people understand what & does
	// 0 0 0 0 0 0 0 35
	size_t iPointerAsNumber = (size_t) iPointer;

	std::cout << iPointerAsNumber << std::endl;
	std::cout << (*iPointer) << std::endl;

	// 0 0 0 0 0 0 0 43
	int* arr1Pointer = iPointer + 2; // explain pointer arithmetic, with pictures
	std::cout << *arr1Pointer;

	return 0;
}

