from __future__ import print_function

import logging
import grpc
import bookInventory_pb2
import bookInventory_pb2_grpc


def get_book_detail(stub, isbn):
    response = stub.GetBook(bookInventory_pb2.GetBookRequest(ISBN=isbn))
    print(response)


def create_new_book(stub):
    book_detail = {
        "ISBN": "978-1-60309-492-4",
        "title": "The Delicacy",
        "author": "James Albon",
        "genre": "HORROR",
        "publishing_year": 2020
    }
    response = stub.CreateBook(bookInventory_pb2.CreateBookRequest(bookDetail=book_detail))
    print(response)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bookInventory_pb2_grpc.InventoryServiceStub(channel)
        print("--------------Book Detail--------------")
        get_book_detail(stub, '978-1-60309-454-2')
        print("--------------Create Result--------------")
        create_new_book(stub)
        print("--------------Book Detail--------------")
        get_book_detail(stub, '978-1-60309-492-4')


if __name__ == '__main__':
    logging.basicConfig()
    run()
