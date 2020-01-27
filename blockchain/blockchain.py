# Blockchain algorithm
from hashlib import sha256
from PyPDF2 import PdfFileReader
import numpy as np

PAGE_ITERATION = 5
BLOCK_LOOP_ITERATIONS = 0

pdf_file_path = input("Which file you want to proceed into the blockchain ? (copy/paste file path)\n")
# pdf_file_page_number = int(input("Page # ?\n"))

pdf_file = open(pdf_file_path, 'rb')
pages_list = list()
pages_range = list()


def get_page_content(file, page_num):
    pdf_reader = PdfFileReader(file)
    page_content = pdf_reader.getPage(page_num).extractText()
    return page_content


def get_pdf_num_pages(file):
    pdf_reader = PdfFileReader(file)
    num_pages = pdf_reader.getNumPages()
    return num_pages


def hash_page_content(file, page_num):
    pdf_reader = PdfFileReader(file)
    page_content = pdf_reader.getPage(page_num).extractText()
    hash_content = sha256(bytes(page_content, "utf8")).hexdigest()
    print("Page # : " + str(page_num + 1))
    print("Content hash : " + hash_content)
    print("Content preview : " + page_content[0:50] + "...")


def page_treatment(file):
    page_number = get_pdf_num_pages(file)
    page_range = np.arange(0, page_number, PAGE_ITERATION)

    for i in page_range:
        pages_range.clear()
        for n in range(i, i + PAGE_ITERATION):
            if n <= page_number:
                pages_range.append(n)
        print(pages_range)
        print("--------")
    # pdf_reader = PdfFileReader(file)


page_treatment(pdf_file_path)
# print(pages_list)

# Loop through each page and execute hash function
#for i in range(get_pdf_num_pages(pdf_file)):
#    hash_page_content(pdf_file, i)

# Close opened file
pdf_file.close()
