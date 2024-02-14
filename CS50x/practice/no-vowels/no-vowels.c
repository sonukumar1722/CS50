// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

// change the vowels
string replace( string word);

int main(int argc, string argv[])
{
    if (argc <= 1 || argc > 2)
    {
        printf("Usage: ./no-vowels word\n");
        return 1;
    }

    string converted = replace(argv[1]);
    printf("%s\n", converted);

    return 0;
}


string replace(string word)
{
    int i = 0;

    while (word[i])
    {
        switch(toupper(word[i]))
        {
            case 'A': {
                word[i] = '6';
                break;
            }
            case 'E': {
                word[i] = '3';
                break;
            }
            case 'I': {
                word[i] = '1';
                break;
            }
            case 'O': {
                word[i] = '0';
                break;
            }
        }
        i++;
    }

    return word;
}
