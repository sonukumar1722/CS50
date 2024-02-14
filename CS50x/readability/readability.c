#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    int letters;
    int words;
    int sentences;
    int index;

    // prompts user for text input
    string text = get_string("Text: ");

    // count the letter
    letters = count_letters(text);
    // printf("%i letters\n", letters);

    // count the word
    words = count_words(text);
    // printf("%i words\n", words);

    // count the sentences
    sentences = count_sentences(text);
    // printf("%i sentences\n", sentences);

    float L = (float)letters / (float) words * 100;
    float S = (float)sentences / (float) words * 100;

    index = (int)round(0.0588 * L - 0.296 * S - 15.8);

    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

    return 0;
}

// count the letter
int count_letters(string text)
{
    int count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] > 64 && text[i] < 91) || (text[i] > 96 && text[i] < 123))
        {
            count++;
        }
    }
    return count;
}

// count the words
int count_words(string text)
{
    int count = 0;
    int i = 0;

    while (text[i])
    {
        if (text[i] == ' ')
        {
            count++;
        }
        i++;
    }
    return count + 1;
}

// count the sentences
int count_sentences(string text)
{
    int count = 0;
    int i = 1;

    while (text[i])
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
        i++;
    }

    return count;
}