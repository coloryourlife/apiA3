import book_pb2_grpc, book_pb2
import grpc


class InventoryClient:
    def __init__(self, server_address, port_number):
        self.server_address = server_address
        self.port_number = port_number
        self.host = server_address + ':' + str(port_number)

    def get_book_details(self, isbn):
        with grpc.insecure_channel(self.host) as channel:
            stub = book_pb2_grpc.InventoryServiceStub(channel)
            return stub.GetBook(book_pb2.GetBookRequest(ISBN=isbn))
