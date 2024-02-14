#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        // Prompts for user input
        height = get_int("Height: ");
        // Check the condition height be in between 1 to 8 (both inclusive)
    }
    while (height < 1 || height > 8);

    // Iteration i for rows
    for (int i = 1; i <= height; i++)
    {
        // Iteration j for columns
        for (int j = height; j > i; j--)
        {
            printf(" ");
        }
        // Iteration k for hashes
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
