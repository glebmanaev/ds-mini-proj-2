import grpc
import bookstore_pb2
import bookstore_pb2_grpc

import pickle
from sklearn.ensemble import RandomForestRegressor

def run():
    with grpc.insecure_channel("localhost:50055") as channel:
        stub = bookstore_pb2_grpc.BookStoreStub(channel)

        price_model = pickle.load(open("ml-price-predicting-model.pkl", "rb"))
        genres_to_onehot = {"biography": [1,0,0,0], "education": [0,1,0,0], "fiction": [0,0,1,0], "non-fiction": [0,0,0,1]}

        while True:
            command = input("Enter a command: ").strip()
            if not command:
                continue

            parts = command.split()
            if parts[0] == "Local-store-ps":
                if len(parts) < 2:
                    print("Usage: Local-store-ps <k>")
                    continue
                try:
                    k = int(parts[1])
                except ValueError:
                    print("Invalid value for k")
                    continue
                response = stub.LocalStorePs(bookstore_pb2.LocalStorePsRequest(k=k))
                print(response.message)

            elif parts[0] == "Create-chain":
                response = stub.CreateChain(bookstore_pb2.CreateChainRequest())
                print(response.message)

            elif parts[0] == "List-chain":
                response = stub.ListChain(bookstore_pb2.ListChainRequest())
                print(response.chain)

            elif parts[0] == "Write-operation":
                if len(parts) < 3:
                    print("Usage: Write-operation <book_name> <price>")
                    continue
                try:
                    price = float(parts[-1])
                except ValueError:
                    print("Invalid price value")
                    continue
                book_name = " ".join(parts[1:-1])
                response = stub.WriteOperation(bookstore_pb2.WriteOperationRequest(book_name=book_name, price=price))
                print(f"{response.book_name} = {response.price} EUR")

            elif parts[0] == "Write-ml":
                if len(parts) < 5:
                    print("Usage: Write-operation <book_name> <year> <pages> <genre>")
                    continue
                book_name = " ".join(parts[1:-3])
                ml_input = [int(parts[-3]), int(parts[-2])] + genres_to_onehot[parts[-1].lower()]
                price = price_model.predict([ml_input])[0]
                price = round(price, 2)
                response = stub.WriteOperation(bookstore_pb2.WriteOperationRequest(book_name=book_name, price=price))
                print(f"{response.book_name} = {response.price} EUR")

            elif parts[0] == "List-books":
                response = stub.ListBooks(bookstore_pb2.ListBooksRequest())
                for i, book in enumerate(response.books):
                    print(f"{i+1}) {book.name} = {book.price} EUR")

            elif parts[0] == "Read-operation":
                if len(parts) < 2:
                    print("Usage: Read-operation <book_name>")
                    continue
                book_name = " ".join(parts[1:])
                response = stub.ReadOperation(bookstore_pb2.ReadOperationRequest(book_name=book_name))
                if response.price > 0:
                    print(f"{book_name} = {response.price} EUR")
                else:
                    print(f"{book_name} not yet in stock")

            elif parts[0] == "Set-timeout":
                # TODO: Implement Set-timeout command
                print("Command not yet implemented")

            elif parts[0] == "Data-status":
                response = stub.DataStatus(bookstore_pb2.DataStatusRequest())
                for i, data_item in enumerate(response.data_items):
                    status = "dirty" if data_item.is_dirty else "clean"
                    print(f"{i+1}) {data_item.name} - {status}")

            elif parts[0] == "Remove-head":
                response = stub.RemoveHead(bookstore_pb2.RemoveHeadRequest())
                print(response.chain)

            elif parts[0] == "Restore-head":
                # TODO: Implement Restore-head command
                print("Command not yet implemented")

            else:
                print(f"Unknown command: {parts[0]}")

if __name__ == '__main__':
    run()