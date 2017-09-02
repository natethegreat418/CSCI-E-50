/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */
 
#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        for (int i = 1; i < d+1; i++)
        {
            for (int j = 1; j < d+1; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();
        
        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(300000);
        }
        else
        {
            printf("\nMove Accepted.\n");
            usleep(300000);
        }

        // sleep thread for animation's sake
        usleep(200000);
    }
    
    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(1000000);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */
void init(void)
{
    //Loop through columns and rows for given dimensions, save data to board array
    int pn = (d*d)-1;
    for (int c = 1; c < d+1; c++)
    {
        for (int r = 1; r < d+1; r++)
        {
            board[c][r] = pn;
            pn--;
        }  
    }
}

/**
 * Prints the board in its current state.
 */
void draw(void)
{
    for (int c = 1; c < d+1; c++)
    {
        for (int r = 1; r < d+1; r++)
        {
            //Replace zero with _
            if (board[c][r]==0)
            {
                printf(" _");
            }
            //Print board as stored in array
            else
            {
                printf( "%2i", board[c][r]); 
            }
            if (r < d)
            {
                printf("|");
            }
        }  
        printf("\n");
    }
}

/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)
{
    //Zero location variables
    int bc = 0;
    int br = 0;
    //Chosen move tile location variables
    int tc = 0;
    int tr = 0;
    for (int c = 1; c < d+1; c++)
    {
        for (int r = 1; r < d+1; r++)
        {
            //Find chosen tile and assign to location variables
            if (board[c][r] == tile)
            {
                tc = c;
                tr = r;
            }
            //Find zero and assign to location variables
            if (board[c][r] == 0)
            {
                bc = c;
                br = r;
            }
        }
    }
    //Determine legality of move and swap values
    int swap = 0;
    if ((abs((tc - bc)) == 1 && abs((tr - br)) == 0) || (abs((tr - br)) == 1 && abs((tc - bc)) == 0))
    {
        swap = board[tc][tr];
        board[tc][tr] = board[bc][br];
        board[bc][br] = swap;
        return true;
        
    }
    //Prohibt move
    else
    {
        return false;
    }
    
}

/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)
{
    //Loop through board
    int sd = 1;
    for (int c = 1; c < d+1; c++)
    {
        for (int r = 1; r < d+1; r++)
        {
            //Compare array value to increment
            if(board[c][r] == sd)
            {
                sd++;
            }
            //Increment value has reach total allowed by dimensions = game won
            else if (sd == d*d)
            {
                return true;
            }
            else
            {
                return false;  
            }
        }
    }
    return false;
}
