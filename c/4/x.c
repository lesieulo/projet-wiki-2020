#include "stdafx.h"
#include <iostream>

#define DLLEXPORT extern "C" __declspec(dllexport)

DLLEXPORT int getResponse(int*& hash_list)
{

    std::cout << hash_list << std::endl;

    int* hashes = new int[3];
    hashes[0] = 8;
    hashes[1] = 9;
    hashes[2] = 10;
    hash_list = hashes;

    std::cout << hash_list << std::endl;
    std::cout << *hash_list << std::endl;
    std::cout << *(hash_list + 1) << std::endl;
    std::cout << *(hash_list + 2) << std::endl;

    return 0;
}

DLLEXPORT void testDLL()
{
    std::cout << "DLL can be read" << std::endl;
}
