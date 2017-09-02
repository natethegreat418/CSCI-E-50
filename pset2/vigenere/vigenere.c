#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main (int argc, string argv[])
{
    //limit to two command line values
    if (argc != 2)
    {
        printf("Inappropriate command line arguments\n");
        return 1;
    }
    //fetch command line input and store length
    string k = argv[1];
    int lena = strlen(k);
    //limit command line value to text
    int g = 0;
    for (int f = 0; f<strlen(k); f++)
    {
        if(isdigit(k[f])){
         g++;   
        }
    }
    if (g>0)
    {
        printf("Inappropriate command line arguments\n");
        return 1;
    }
    //normal program operation
    else 
    {
        //collect plaintext input and store length
        printf("plaintext: ");
        string p = get_string();
        int lens = strlen(p);
        printf("ciphertext: ");
        //array control
        int j = 0;
        //iterate through plaintext input
        for (int i = 0; i < lens; i++)
        {
            //separate non-alphabet characters
            if (isalpha(p[i]))
                    {
                    //separate upper-case characters
                    if (isupper(p[i]))
                        {
                        //iterate through array values and choose appropriate
                        int ml = j%lena;
                        //normalize array value to current case
                        char uc = toupper(k[ml]);
                        //find alphavalue for key value
                        int c = (uc)-65;
                        //find alphavalue for plaintext value
                        int cb = p[i]-65;
                        //find outset amount
                        int cp = ((c+cb)%26);
                        //apply offset to character and print
                        int cc = cp+65;
                        printf("%c",cc);
                        j++;
                        }
            
                    if (islower(p[i]))
                        {
                        //iterate through array values and choose appropriate
                        int ml = j%lena;
                        //normalize array value to current case
                        char lc = tolower(k[ml]);
                        //find alphavalue for key value
                        int c = (lc)-97;
                        //find alphavalue for plaintext value
                        int cb = p[i]-97;
                        //find outset amount
                        int cp = ((c+cb)%26);
                        //apply offset to character and print
                        int cc = cp+97;
                        printf("%c",cc);
                        j++;
                        }
                    }
            else
            {
                printf("%c",p[i]);
            }
        }
    printf("\n");
    }
}
