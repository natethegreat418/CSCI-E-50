#include <stdio.h>
#include <cs50.h>   

int main(void)
{
    int cardnum = 100;
    for (int loops=1; loops<cardnum; loops++)
    {
        int mod = 2*loops;
        printf("%i\n", mod);
    }
}