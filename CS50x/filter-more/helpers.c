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
                    else
                    {
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

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    int redX = 0;
    int blueX = 0;
    int greenX = 0;

    int redY = 0;
    int blueY = 0;
    int greenY = 0;

    int x = 0;
    int y = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            redX = blueX = greenX = 0;
            redY = blueY = greenY = 0;


            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    int row = i + k;
                    int col = j + l;

                    if (row < 0 || row > height - 1 || col < 0 || col > width - 1)
                    {
                        continue;
                    }

                    redX += Gx[k + 1][l + 1] * image[row][col].rgbtRed;
                    blueX += Gx[k + 1][l + 1] * image[row][col].rgbtBlue;
                    greenX += Gx[k + 1][l + 1] * image[row][col].rgbtGreen;

                    redY += Gy[k + 1][l + 1] * image[row][col].rgbtRed;
                    blueY += Gy[k + 1][l + 1] * image[row][col].rgbtBlue;
                    greenY += Gy[k + 1][l + 1] * image[row][col].rgbtGreen;

                }
            }

            temp[i][j].rgbtRed = round(sqrt(redX * redX + redY * redY)) > 255 ? 255 : round(sqrt(redX * redX + redY * redY));
            temp[i][j].rgbtBlue = round(sqrt(blueX * blueX + blueY * blueY)) > 255 ? 255 : round(sqrt(blueX * blueX + blueY * blueY));
            temp[i][j].rgbtGreen = round(sqrt(greenX * greenX + greenY * greenY)) > 255 ? 255 : round(sqrt(greenX * greenX + greenY * greenY));
        }
    }

    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            image[k][l] = temp[k][l];
        }
    }
    return;
}
