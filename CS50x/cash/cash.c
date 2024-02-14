#include <cs50.h>
#include <stdio.h>

int main()
{
    // Prompt the user for cash owed, in cents
    int cents;
    do
    {
        cents = get_int("How much cents you owned? ");
    }
    while (cents < 0);

    // Calculate how many quarters you should give customer
    int quarters = cents / 25;

    // Subtract the value of those quarters from cents
    cents -= quarters * 25;

    // Calculate how many dimes you should give customer
    int dims = cents / 10;

    // Subtract the value of those dimes from remaining cents
    cents -= dims * 10;

    // Calculate how many nickels you should give customer
    int nickels = cents / 5;

    // Subtract the value of those nickels from remaining cents
    cents -= nickels * 5;

    // Calculate how many pennies you should give customer
    int pennis = cents;

    // Subtract the value of those pennies from remaining cents
    cents -= pennis * 5;

    // Sum the number of quarters, dimes, nickels, and pennies used
    int sum = quarters + dims + nickels + pennis;

    // Print that sum
    printf("Sum: %i", sum);

    return 0;
}