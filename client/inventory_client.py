import bookInventory_pb2_grpc
import bookInventory_pb2
import grpc


class InventoryClient:
    def __init__(self, server_address, port_number):
        """
        Get server address and port number when initialize
        Generate host with given address and port number to make stub
        """
        self.server_address = server_address
        self.port_number = port_number
        self.host = server_address + ':' + str(port_number)

    def get_book_details(self, isbn):
        with grpc.insecure_channel(self.host) as channel:
            stub = bookInventory_pb2_grpc.InventoryServiceStub(channel)
            return stub.GetBook(bookInventory_pb2.GetBookRequest(ISBN=isbn))
