#include <stdio.h>
#include <cs50.h>   

int main(void)
{
    printf("Hello! This application is designed to help you calculate your water usage.\n");
    printf("Please indicate in minutes the length of your daily shower (round to nearest whole numbers).\n");
    int min = get_int();
    int bottles = (min*1.5*128)/16;
    printf("Your daily shower lasting %i minutes consumes %i bottles of water.\n", min, bottles);
}   