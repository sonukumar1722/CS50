#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "wav.h"

int check_format(WAVHEADER *header);
int get_block_size(WAVHEADER *header);

int main(int argc, char *argv[])
{
    WAVHEADER header;

    // Ensure proper usage
    if (argc < 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading
    FILE *input = fopen(argv[1], "rb");
    if (input == NULL)
    {
        printf("Failed to open input file\n");
        return 1;
    }

    // Read header
    fread(&header, sizeof(WAVHEADER), 1, input);

    // Use check_format to ensure WAV format
    if (!check_format(&header))
    {
        printf("Invalid WAV format\n");
        return 1;
    }

    // Open output file for writing
    FILE *output = fopen(argv[2], "wb");
    if (output == NULL)
    {
        printf("File not opend!\n");
        return 1;
    }

    // Write header to file
    fwrite(&header, sizeof(WAVHEADER), 1, output);

    // Use get_block_size to calculate size of block
    int block_size = get_block_size(&header);
    BYTE *buffer = malloc(block_size);

    // Write reversed audio to file
    fseek(input, -block_size, SEEK_END); // Move to the last block of data
    while (ftell(input) >= 44)           // Continue until the beginning of the data is reached
    {
        fread(buffer, 1, block_size, input);     // Read a block of data
        fwrite(buffer, 1, block_size, output);   // Write the block of data to the output file
        fseek(input, -2 * block_size, SEEK_CUR); // Move backward by 2 blocks
    }

    fclose(input);
    fclose(output);
    free(buffer);
}

int check_format(WAVHEADER *header)
{

    if (memcmp(header->chunkID, "RIFF", 4) == 0 &&
        memcmp(header->format, "WAVE", 4) == 0 &&
        memcmp(header->subchunk1ID, "fmt ", 4) == 0 &&
        memcmp(header->subchunk2ID, "data", 4) == 0)
    {
        return 1; // Format is valid
    }
    return 0; // Format is invalid
}

int get_block_size(WAVHEADER *header)
{
    return (header->numChannels * header->bitsPerSample) / 8;
}