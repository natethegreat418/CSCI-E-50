#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main (int argc, string argv[])
{
    if (argc == 2)
    {
        printf("plaintext:");
        string t = get_string();
        int k = atoi(argv[1]);
        int lens = strlen(t);
        printf("ciphertext:");
        for (int i = 0; i < lens; i++)
        {
            if (isalpha(t[i]))
            {
                if (isupper(t[i]))
                {
                int m = (t[i]-65);
                int c = ((m+k)%26);
                int l = (c+65);
                printf("%c",l);
                }
            
                if (islower(t[i]))
                {
                int m = (t[i]-97);
                int c = ((m+k)%26);
                int l = (c+97);
                printf("%c",l);
                }
            }
            else
            {
                printf("%c",t[i]);
            }

        
    }
            printf("\n");
            return 0;
    }
    else 
    {
        printf("Inappropriate command line arguments\n");
        return 1;
    }
}
