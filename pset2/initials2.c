#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    //Collect name//
    string s = get_string();
    //Store length of name//
    int n = 1;
    while ((s[n] = 1))
        {
        printf("%c\n", s[n]);
        n++;
            while (s[n] != '\0')
            {
                n++;
            }
        }
        

    printf("%i\n", n);

    }