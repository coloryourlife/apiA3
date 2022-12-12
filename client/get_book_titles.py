from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))  # To resolve module not found error

from client import inventory_client
import logging

isbns = ["978-1-60309-502-0", "978-1-60309-454-2"]


def get_book_titles(client, isbn_list):
    """
    Get detail information of the book via client object
    Extract title from the detail we got from the client object
    """
    title_list = []
    for isbn in isbn_list:
        response = client.get_book_details(isbn)
        title_list.append(response.bookDetail.title)

    return title_list


def run():
    client = inventory_client.InventoryClient('localhost', 50051)   # initiate client object
    res = get_book_titles(client, isbns)    # pass client object as a parameter
    print(res)


if __name__ == '__main__':
    logging.basicConfig()
    run()
