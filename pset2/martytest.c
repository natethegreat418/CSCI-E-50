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
    
    int i = 0;
    while (i < lens)
    {
        if(i == 0) printf("%c", s[i]);
        if (s[i] == ' ')
        {
            int j = i + 1;
            if (s[j] != ' ') {
                printf("%c", s[j]);
            }
        }
        i++;
    }
    
    }