#include <stdlib.h>
#include <stdint.h>
__declspec(dllexport) void read(int16_t* input, size_t size)
{
  int i;
  for(i=0;i<size;i++)
    input[i] = i;
}
