#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);
void decimal_to_binary(int decimal);

int main(void)
{
    // TODO
    string text = get_string("Message: ");
    int length = strlen(text);
    int decimal = 0;
    printf("%s %i\n", text, length);

    for (int i = 0; i < length; i++)
    {
        decimal = text[i];
        decimal_to_binary(decimal);
    }

    return 0;
}

// print the pattern
void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}

// Convert decimal to binary
void decimal_to_binary(int decimal)
{
    int binary[BITS_IN_BYTE * 2];
    int i = 0;

    for (int k = 0; k < BITS_IN_BYTE; k++)
    {
        binary[k] = 0;
    }

    while (decimal != 0)
    {
        binary[i] = decimal % 2;
        decimal = decimal / 2;
        i++;
    }

    for (int j = BITS_IN_BYTE - 1; j >= 0; j--)
    {
        print_bulb(binary[j]);
    }
    printf("\n");
}
