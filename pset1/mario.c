#include <stdio.h>
#include <cs50.h>   

int main(void)
{
    printf("Please indicate the height of the half-pyramid\n");
    int height;
    height = get_int();
    while (height<0 || height>23)
    {
        printf("Please indicate the height of the half-pyramid\n");
        height = get_int();
    }
    for (int row =1; row<height+1; row++)
    {
        for (int s=0; s<height-row; s++)
        {
        printf(" ");
        }
        for (int h=0; h<1+row; h++)
        {
        printf("#");
        }
        printf("\n");
        
    }
}