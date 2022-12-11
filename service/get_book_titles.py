import inventory_client
import logging
import book_pb2

isbns = ["978-1-60309-502-0", "978-1-60309-454-2"]


def protobuf_to_dict(proto_obj):
    key_list = proto_obj.DESCRIPTOR.fields_by_name.keys()
    d = {}
    for key in key_list:
        d[key] = getattr(proto_obj, key)
    return d


def get_book_titles(client, isbn_list):
    title_list = []
    for isbn in isbn_list:
        response = client.get_book_details(isbn)
        print(response.ParseFromString())
        # title_list.append(dict_res.title)

    return title_list


def run():
    client = inventory_client.InventoryClient('localhost', 50051)
    res = get_book_titles(client, isbns)
    print(res)


if __name__ == '__main__':
    logging.basicConfig()
    run()
