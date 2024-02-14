from cs50 import get_string


def main():
    # variable declaration
    para = get_string("Text: ")
    lettersc = count_letters(para)
    wordsc = count_words(para)
    sentencesc = count_sentences(para)

    # To calculate the grade
    L = (lettersc / wordsc) * 100
    S = (sentencesc / wordsc) * 100

    # Roundingoff the grade
    graded = round(0.0588 * L - 0.296 * S - 15.8)

    if graded < 1:
        print("Before Grade 1")

    elif graded > 16:
        print("Grade 16+")

    else:
        print(f"Grade {graded}")


# Calculate the number of charaters in the text
def count_letters(text):
    counter = 0

    # Looping through the word
    for i in range(len(text)):
        if text[i].islower() or text[i].isupper():

            # Counting the character in the word
            counter += 1

    return counter


# Calculate the  number of words in the text
def count_words(text):
    counter = 0

    # Looping through the sentence in the textfile
    for i in range(len(text)):
        if text[i] == ' ':

            # counting the words in the text
            counter += 1

    return counter + 1

# Calculate the number of sentences in the text


def count_sentences(text):
    counter = 0

    # Looping through the text in the text file
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':

            # Counting the sentences in the textfile
            counter += 1

    return counter


# Main function
if __name__ == "__main__":
    main()
