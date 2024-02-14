#include "helpers.h"
#include "math.h"
#include "stdio.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = round((image[i][j].rgbtGreen + image[i][j].rgbtBlue + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int red, green, blue;
    float rgbtGreen, rgbtBlue, rgbtRed;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            rgbtRed = image[i][j].rgbtRed;
            rgbtGreen = image[i][j].rgbtGreen;
            rgbtBlue = image[i][j].rgbtBlue;

            red = round(.393 * rgbtRed + .769 * rgbtGreen + .189 * rgbtBlue);
            green = round(.349 * rgbtRed + .686 * rgbtGreen + .168 * rgbtBlue);
            blue = round(.272 * rgbtRed + .534 * rgbtGreen + .131 * rgbtBlue);

            image[i][j].rgbtRed = red > 255 ? 255 : red;
            image[i][j].rgbtGreen = green > 255 ? 255 : green;
            image[i][j].rgbtBlue = blue > 255 ? 255 : blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = width - 1; j >= 0; j--)
        {
            temp[i][width - j - 1] = image[i][j];
        }
        for (int k = 0; k < width; k++)
        {
            image[i][k] = temp[i][k];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    int Red = 0;
    int Blue = 0;
    int Green = 0;
    float count = 0.0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            for (int k = i - 1; k < i + 2; k++)
            {
                for (int l = j - 1; l < j + 2; l++)
                {
                    if (k < 0 || k > height - 1 || l < 0 || l > width - 1)
                    {
                        continue;
                    }
                    else{
                        Red += image[k][l].rgbtRed;
                        Blue += image[k][l].rgbtBlue;
                        Green += image[k][l].rgbtGreen;
                        count++;
                    }
                }
            }

            temp[i][j].rgbtRed = round(Red / count);
            temp[i][j].rgbtBlue = round(Blue / count);
            temp[i][j].rgbtGreen = round(Green / count);

            Red = 0;
            Blue = 0;
            Green = 0;
            count = 0.0;
            }
        }

        for (int i = 0; i < height; i++)
        {
            for (int j = 0; j < width; j++)
            {
                image[i][j] = temp[i][j];
            }
        }

    return;
}
