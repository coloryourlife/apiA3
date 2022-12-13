from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))  # To resolve module not found error

from concurrent import futures
import logging

import grpc

from service.bookInventory_pb2 import (
    Genre,
    Book,
    ResponseStatus,
    GetBookResponse,
    CreateBookResponse
)
from service import bookInventory_pb2_grpc

"""
Key: ISBN, Value: Book
"""
books = {
    "978-1-60309-502-0": Book(ISBN="978-1-60309-502-0", title="Animal Stories", author="Peter Hoey", genre=Genre.DRAMA, publishing_year=2022),
    "978-1-60309-454-2": Book(ISBN="978-1-60309-454-2", title="Cosmoknights", author="Hannah Templer", genre=Genre.FANTASY, publishing_year=2021)
}


class InventoryServicer(bookInventory_pb2_grpc.InventoryServiceServicer):
    """
    GetBook(self, request, context)
    If the given ISBN is not found in our storage return GetBookResponse with a 404 error message
    Else return GetBookResponse with bookDetail
    """
    def GetBook(self, request, context):
        if request.ISBN not in books:
            return GetBookResponse(bookDetail=None, status=ResponseStatus(code=404, message="Book not found"))

        book = books.get(request.ISBN)

        return GetBookResponse(bookDetail=book, status=ResponseStatus(code=200, message="Successfully find"))

    """
    CreateBook(self, request, context)
    if one of ISBN, author, title is empty return error message. (Assumed those three data is essential)
    if given ISBN already exists in our storage return CreateBookResponse with a 403 error message
    else create a book and store in our storage, return CreateBookResponse with success message
    """
    def CreateBook(self, request, context):
        book_detail = request.bookDetail

        if not(book_detail.ISBN and book_detail.author and book_detail.title):
            return CreateBookResponse(status=ResponseStatus(code=406, message="Need more information"))

        if book_detail.ISBN in books:
            return CreateBookResponse(status=ResponseStatus(code=403, message="Already exists"))

        new_book = Book(
            ISBN=book_detail.ISBN,
            title=book_detail.title,
            author=book_detail.author,
            genre=book_detail.genre,
            publishing_year=book_detail.publishing_year
        )

        books[book_detail.ISBN] = new_book

        return CreateBookResponse(status=ResponseStatus(code=200, message="Successfully created"))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    bookInventory_pb2_grpc.add_InventoryServiceServicer_to_server(
        InventoryServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started. listening on 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
