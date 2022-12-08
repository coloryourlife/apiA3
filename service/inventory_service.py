from concurrent import futures
import logging

import grpc

from book_pb2 import (
    Genre,
    Book,
    GetBookResponse,
    CreateBookResponse
)
import book_pb2_grpc

books = {
    "978-1-60309-502-0": Book(ISBN="978-1-60309-502-0", title="Animal Stories", author="Peter Hoey", genre=Genre.DRAMA, publishing_year=2022),
    "978-1-60309-454-2": Book(ISBN="978-1-60309-454-2", title="Cosmoknights", author="Hannah Templer", genre=Genre.FANTASY, publishing_year=2021)
}


class InventoryServicer(book_pb2_grpc.InventoryServiceServicer):
    def GetBook(self, request, context):
        if request.ISBN not in books:
            context.abort(grpc.StatusCode.NOT_FOUND, "Book not found")

        book = books.get(request.ISBN)

        return GetBookResponse(bookDetail=book)

    def CreateBook(self, request, context):
        book_detail = request.bookDetail

        if book_detail.ISBN in books:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "Already exists")

        new_book = Book(
            ISBN=book_detail.ISBN,
            title=book_detail.title,
            author=book_detail.author,
            genre=book_detail.genre,
            publishing_year=book_detail.publishing_year
        )

        books[book_detail.ISBN] = new_book
        print(books)

        return CreateBookResponse(responseMsg="Successfully Created")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    book_pb2_grpc.add_InventoryServiceServicer_to_server(
        InventoryServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started. listening on 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
