#include <stdio.h>
#include <cs50.h>   

int main(void)
{
    printf("Oh hey! How much change is owed?\n");
    float owed;
    owed = get_float();
    while (owed<=0)
        {
        printf("How much change is owed?\n");
        owed = get_float();
        }
    int owedc = (owed+.005)*100;
    int coinsused=0;
    while(owedc >= 25)
    {
        owedc = owedc - 25;
        coinsused++;
    }    
    while(owedc >= 10)
    {
        owedc = owedc - 10;
        coinsused++;
    }
    while(owedc >= 5)
    {
        owedc = owedc - 5;
        coinsused++;
    }
    while(owedc >= 1)
    {
        owedc = owedc - 1;
        coinsused++;
    }
    printf("%i\n",coinsused);
}