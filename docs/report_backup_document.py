from docx.document import Document
# from docx.shared import Inches


# global lists to store document metadata

heading_one = []  # all major headings in the doc (h1)
heading_two = []  # all headings with h2


def get_doc():
    word_file = Document('examples/example1.docx')

    # Extracting all headings and paragraphs
    for attributes in word_file.paragraphs:
        if attributes.style.name == 'Heading 1':
            heading_one.append(attributes.text)
        else:
            heading_two.append(attributes.text)

    return heading_one, heading_two
