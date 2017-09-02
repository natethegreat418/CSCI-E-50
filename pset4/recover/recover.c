/**
 * Locates and recovers JPG images off of a raw data file.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure appropriate command line arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile(raw data source)\n");
        return 1;
    }
    
    // store input file name
    char *infile = argv[1];
    
    // check to pen input file 
    FILE *input = fopen(infile, "r");
    if (input == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    
    // storage for fread
    BYTE *buffer = malloc(sizeof(BYTE)*64);
    
    //loop control
    int ff = 0;
    
    // file parameters
    char name[8];
    FILE *img;
    
    // cycle through data in groups of chunks of 512bits
    while (fread(buffer, sizeof(buffer), 1, input) == 1)
    {
        // identify the start of a JPG
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // open file for first found JPG
            if (ff == 0)
            {
                sprintf(name, "%03i.jpg", ff);
                img = fopen(name, "w");
                fwrite(buffer, sizeof(buffer), 1, img);
                ff++;
            }
            
            // handle (close preceeding, open new) subsequent JPGs
            else if (ff > 0)
            {
                fclose(img);
                sprintf(name, "%03i.jpg", ff);
                img = fopen(name, "w");
                fwrite(buffer, sizeof(buffer), 1, img);
                ff++;
            }
        }
        else 
        {
            // continue writing if open file
            if (ff > 0)
            {
                fwrite(buffer, sizeof(buffer), 1, img);
            }
        }
    }
    return 0;
}
    