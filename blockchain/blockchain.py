# Blockchain algorithm
from hashlib import sha256
from PyPDF2 import PdfFileReader


PAGE_ITERATION = 5

pdf_file_path = input("Which file you want to proceed into the blockchain ? (copy/paste file path)\n")
pdf_file_page_number = int(input("Page no. ?\n"))

pdf_file = open(pdf_file_path, 'rb')
pages_list_selected = list()
transactions = list()
pages_range = list()


def get_pdf_num_pages(file):
    pdf_reader = PdfFileReader(file)
    num_pages = pdf_reader.getNumPages()
    return num_pages


def get_page_content(file, page_num):
    pdf_reader = PdfFileReader(file)
    page_content = pdf_reader.getPage(page_num).extractText()
    return page_content


def hash_page_content(file, page_num):
    page_content = get_page_content(file, page_num)
    hashed_content = sha256(bytes(page_content, "utf8")).hexdigest()
    transactions.append(hashed_content)
    print("Page # : " + str(page_num))
    print("Content hash : " + hashed_content)
    print("Content preview : " + page_content[0:100] + "...")


def pages_treatment(file, page):
    if page % PAGE_ITERATION == 0:
        num_pages = get_pdf_num_pages(file)

        for i in range(page, page + PAGE_ITERATION):
            if i <= num_pages:
                pages_list_selected.append(i)
                hash_page_content(file, i)
    else:
        print("Error !")


def new_block():
    # New block algorithm
    print("New block")


def add_block_to_blockchain():
    # Add block to the blockchain
    print("Add")


def main():
    # Select only requested pages
    pages_treatment(pdf_file_path, pdf_file_page_number)
    print(transactions)


main()

# Close opened file
pdf_file.close()
