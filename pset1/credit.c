#include <stdio.h>
#include <cs50.h>   

int main(void)
{
    long cardnum;
    do
    {
        cardnum = get_long_long();
    }
    while (cardnum<0);
    for (int loops=1; loops<cardnum; loops=loops*100)
    {
        int mod = 100*loops;
        long founddig1 = (cardnum % mod)/(mod/10);
        printf("%ld\n",founddig1);
    }
    for (int loops2=1; loops2<cardnum; loops2=loops2*10)
    {
        int mod2 = 100*loops2;
        long founddig2 = (cardnum % mod2);
        printf("%ld\n",founddig2);
    }
}