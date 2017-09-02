#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    //Collect name//
    string s = get_string();
    //Store length of name//
    int lens = strlen(s);
    //Name control variables
    int n = 0;
    int l = 0;
    //Limit loop to string length
    while (n<lens)
    {
        //Print letter when l is 0 (program start)
        if (l == 0)
        {
        printf("%c",toupper(s[n]));
        l++;
        }
        //Reset print control when blank found
        if (s[n] == ' ')
        {
        l = 0;
        }
    n++;
    }
    printf("\n");
    }