import sys, os
from PIL import Image, ImageOps


def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 3:
        print("Too few command-line arguments")
        sys.exit(1)
    elif len(sys.argv) > 3:
        print("Too many command-line arguments")
        sys.exit(2)
    # Check if the file extensions are valid
    elif (os.path.splitext(sys.argv[1])[-1] or os.path.splitext(sys.argv[2])[-1]) not in [".jpg", ".jpeg", ".png"]:
        print("Invalid file extension")
        sys.exit(3)
    # Check if the input and output files have the same extension
    elif not sys.argv[1].split(".")[1] == sys.argv[2].split(".")[1]:
        print("Invalid output")
        sys.exit(4)
    # Check if the input and output files have the same extension
    elif not os.path.splitext(sys.argv[1])[-1] == os.path.splitext(sys.argv[2])[-1]:
        print("Input and output have different extensions")
        sys.exit(5)
    # Check if the input file exists
    elif len(sys.argv) == 2:
        print("Input does not exist")
        sys.exit(6)
    else:
        wore_virtual_tshirt()


def wore_virtual_tshirt():
    # Open the virtual t-shirt image (shirt.png)
    shirt = Image.open("shirt.png")
    size = shirt.size
    # Open the input image provided via command-line argument
    with Image.open(sys.argv[1], 'r') as image1:
        # Resize the input image to fit the size of the virtual t-shirt image
        resized_image = ImageOps.fit(image1, size)
        # Paste the virtual t-shirt image onto the resized input image
        resized_image.paste(shirt, box=None, mask=shirt)
        # Save the final image with the provided output filename
        resized_image.save(sys.argv[2], format=None)


if __name__ == "__main__":
    main()
