<<<<<<< HEAD
#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    printf(GREEN"Hello, world"RESET"\n");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    int i = 0;
    int scores = 0;

    while (word[i])
    {
        if ((word[i] > 64 && word[i] < 91) || (word[i] > 96 && word[i] < 123))
        {
            scores += POINTS[65 - toupper(word[i])];
        }
        i++;
    }

    return scores;
}
=======
#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    printf(GREEN"Hello, world"RESET"\n");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    int i = 0;
    int scores = 0;

    while (word[i])
    {
        if ((word[i] > 64 && word[i] < 91) || (word[i] > 96 && word[i] < 123))
        {
            scores += POINTS[65 - toupper(word[i])];
        }
        i++;
    }

    return scores;
}
>>>>>>> 58830397b36a3a69919710186cb0219cf3d88e5b
