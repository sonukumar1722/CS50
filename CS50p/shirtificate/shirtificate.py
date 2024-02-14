from fpdf import FPDF

def main():
    # Prompt user for name
    name = input("Name: ")

    # Create a new PDF object with specified orientation, unit, and format
    pdf = FPDF(orientation="P", unit='mm', format=(210, 297))

    # Add a new page to the PDF
    pdf.add_page()

    # Set the font family and size for the PDF
    pdf.set_font(family='helvetica', size=48)

    # Add a cell with the text "CS50 Shirtificate"
    pdf.cell(txt="CS50 Shirtificate", w=0, h=56, align="C", new_x='START', new_y="NEXT")

    # Add an image to the PDF
    pdf.image(name='shirtificate.png', x="C", y=60.0)

    # Set the font family and size for the PDF
    pdf.set_font(family='helvetica', size=24)

    # Set the text color to white
    pdf.set_text_color(255, 255, 255)

    # Set the position for the following text
    pdf.set_xy(0, -175)

    # Add a cell with the name and the text "took CS50"
    pdf.cell(txt=f"{name} took CS50", w=0, align='C')

    # Disable automatic page breaks
    pdf.set_auto_page_break(False)

    # Output the PDF file with the given name
    pdf.output("shirtificate.pdf")


if __name__ == '__main__':
    main()
