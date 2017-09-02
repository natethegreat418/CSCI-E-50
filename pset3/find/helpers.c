/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <stdio.h> 
#include <cs50.h>
#include <math.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    //Begin search, check if array length is less than 1
    printf("Begin search\n");
    if(n > 0)
    {
        //Check if array length is equal to 1
        if (n < 2)
        {
            //If array length == 1, compare sole array value to needle value
            if (values[n] == value)
            {
                return true;   
            }
            else
            {
                return false;
            }
        }
        //Where array length is > 1, commit search 
        else
        {
            //Define control variables
            int c = 0;
            int rb = n;
            int lb = n-n;
            int smid = (floor((rb-lb)/2)-1);
            //Initiate loop
            while (c < n)
            {
                //Case: Mid = sought value
                if (values[smid] == value)
                {
                    return true;
                }
                //Case: Mid greater than sought value
                else if (values[smid] > value)
                {
                    c++;
                    rb = smid-1;
                    smid = (rb+lb)/2;
                }
                //Case: Mid less than sought value
                else if (values[smid] < value)
                {
                    c++;
                    lb = smid+1;
                    smid = (rb+lb)/2;
                }
            }
        }
        return false;
    }
    //Return 'false' if array less than 1 
    else
    {
        return false;
    }
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    //Loop through whole array
    for (int i = 0; i < n; i++)
        {
            int swap = 0;
            int min = values[i];
            //From each array value, move through the array
            for(int k = i+1; k < n; k++)
            {
                //Find lowest value
                if (values[k] < min)
                {
                    min = values[k];
                    swap = k;
                }
            }
            //Swap array position for lowest value
            if (swap != 0)
            {
                values[swap] = values[i];
                values[i] = min;
            }
        }
    return;
}