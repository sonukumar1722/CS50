#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Defining the data type BYTE
    typedef uint8_t BYTE;
    // Allocating the mermory for storing the name of image file
    char *name = malloc(8);
    if (name == NULL)
    {
        free(name);
        printf("No space\n");
        return 1;
    }

    // Checks the validation for commmanf-line input
    if (argc != 2)
    {
        free(name);
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Oepning the forensic image file
    FILE *file = fopen(argv[1], "r");

    // Checks vaidaton for forensic file existence
    if (!file)
    {
        free(name);
        printf("Forensic image can't open\n");
        return 1;
    }

    FILE *images;
    BYTE buffer[512];
    // Counter to store the numerical part of image name
    int i = 0;
    // Checks if image file is open or close (1 or 0)
    int fileStatus = 1;
    // Indicate wheter to read bytes form forensiz image file or not (1 or 0)
    int read = 0;

    while (fread(buffer, sizeof(BYTE), 512, file) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && fileStatus == 0)
        {
            // closing the image file
            fclose(images);
            read = 0;
            fileStatus = 1;
        }
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && fileStatus == 1)
        {
            // Formatting the name of image file
            sprintf(name, "%03i.jpg", i);
            // Opening the image file
            images = fopen(name, "w");
            i += 1;
            fileStatus = 0;
            read = 1;
        }
        if (read)
        {
            // Writing bytes into the image file
            fwrite(buffer, sizeof(BYTE), 512, images);
        }
    }

    // free the memory
    free(name);
    // Closing the file
    fclose(file);
    // close images file
    fclose(images);
}