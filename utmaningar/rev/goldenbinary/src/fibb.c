#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define SQRT(x) pow(x, 0.5)

uint16_t fibonacci(uint16_t n)
{
    return (uint16_t)((pow(1+SQRT(5), n)-pow(1-SQRT(5), n))/(pow(2, n)*SQRT(5)));
}

uint16_t fibEncode(uint16_t n)
{
    uint16_t ret = 0; 
    if(n == 0)
    {
        // fibonacci encoding for 256
        return 0b0001100001000010;
    }
    
    while(n != 0)
    {
        uint8_t i = 0;
        while(n >= fibonacci(i+2))
        {
            i++;
        }
        if(ret == 0)
        {
            ret |= 1 << i;
            i--;
            ret |= 1 << i;
        }else
        {
            i--;
            ret |= 1 << i; 
        }
        n = n - fibonacci(i+2);
    }
    return ret;
}

void fibEncodeFILEXOR(FILE * in, FILE * out)
{
    size_t bitIndex = 7;
    uint8_t bit = 0;
    uint8_t tempout = 0;
    int tempin = 0;
    uint8_t xorValue = 0xFF;
    while((tempin = fgetc(in)) != EOF)
    {
        uint16_t encoded = fibEncode(xorValue^((uint8_t)tempin));
        xorValue = 0;
        //printf("encoded = %d, bitIndex = %ld\n",encoded ,bitIndex);
        while(encoded != 0){
            uint8_t bit = encoded & 0b1;
            encoded >>= 1;
            xorValue = (xorValue<<1)|bit;
            if(bit){
                tempout |= bit << bitIndex;
            }
            bitIndex--;
            if(bitIndex > 7)
            {
                bitIndex = 7;
                fputc(tempout, out);
                tempout = 0;
            }
        }
    }

    if(bitIndex != 7)
    {
        fputc(tempout, out);
    }

}

int main(int argc, char ** argv)
{
    if(argc < 3)
    {
        printf("usage: %s INPUT-FILE OUTPUT-FILE\n", argv[0]);
        return 1;
    }
    
    FILE * in = fopen(argv[1], "rb");
    FILE * out = fopen(argv[2], "wb");
    fibEncodeFILEXOR(in, out);
    return 0;
}
