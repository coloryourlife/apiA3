from unittest.mock import patch, MagicMock
from book_pb2 import Genre, Book, GetBookResponse
from inventory_client import InventoryClient
from get_book_titles import get_book_titles
import unittest

test_book1 = Book(ISBN="test1", title="test1 title", author="test1 author", genre=Genre.COMEDY, publishing_year=2021)
test_book2 = Book(ISBN="test2", title="test2 title", author="test2 author", genre=Genre.COMEDY, publishing_year=2021)


class ClientTest(unittest.TestCase):
	"""
	Implemented mock API client with @patch annotation and passed it to the unit test
	Set get_book_details return value with side_effect since it should be called more than one with different return values
	"""
	@patch('inventory_client.InventoryClient')
	def test_get_book_titles_with_mock(self, MockClient):
		client = MockClient()
		client.get_book_details.side_effect = [
			GetBookResponse(bookDetail=test_book1),
			GetBookResponse(bookDetail=test_book2)
		]
		self.assertEqual(get_book_titles(client, ['a', 'b']), ['test1 title', 'test2 title'])

	def test_get_book_titles_with_real_server(self):
		"""
		Unit test for live server
		Passed the exact server_address and port number of server
		Should be tested with real data
		"""
		client = InventoryClient('localhost', 50051)
		isbns = ["978-1-60309-502-0", "978-1-60309-454-2"]
		self.assertEqual(get_book_titles(client, isbns), ["Animal Stories", "Cosmoknights"])


if __name__ == '__main__':
	unittest.main()
