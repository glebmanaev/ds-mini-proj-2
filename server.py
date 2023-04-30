import grpc
from concurrent import futures
import random
import time
import bookstore_pb2
import bookstore_pb2_grpc

class BookStoreService(bookstore_pb2_grpc.BookStoreServicer):
    def __init__(self):
        self.data = {}
        self.chain = []

    def LocalStorePs(self, request, context):
        for i in range(request.k):
            ps_id = f"{context.peer()}-ps{i+1}"
            self.data[ps_id] = {}
        return bookstore_pb2.LocalStorePsResponse(message=f"{request.k} processes created in {context.peer()}")

    def CreateChain(self, request, context):
        if self.chain:
            return bookstore_pb2.CreateChainResponse(message="Chain already exists. Use RemoveHead to remove the current head.")
        if not self.data:
            return bookstore_pb2.CreateChainResponse(message="No processes found. Use LocalStorePs to create processes.")
        self.chain = [random.choice(list(self.data.keys()))]
        while len(self.chain) < len(self.data):
            successors = [k for k in self.data.keys() if k not in self.chain]
            successor = random.choice(successors)
            self.data[self.chain[-1]]["successor"] = successor
            self.data[successor]["predecessor"] = self.chain[-1]
            self.chain.append(successor)
        self.data[self.chain[0]]["head"] = True
        self.data[self.chain[-1]]["tail"] = True
        return bookstore_pb2.CreateChainResponse(message="Chain created successfully")

    def ListChain(self, request, context):
        if not self.chain:
            return bookstore_pb2.ListChainResponse(chain="No chain found. Use CreateChain to create a chain.")
        chain_str = "->".join([f"{ps} (Head)" if self.data[ps].get("head") else f"{ps} (Tail)" if self.data[ps].get("tail") else ps for ps in self.chain])
        return bookstore_pb2.ListChainResponse(chain=chain_str)

    def WriteOperation(self, request, context):
        if not self.chain:
            return bookstore_pb2.WriteOperationResponse(book_name=request.book_name, price=request.price)
        current_ps = self.chain[0]
        for ps in self.chain:
            if self.data[ps].get("head"):
                current_ps = ps
                break
        self.data[current_ps][request.book_name] = (request.price, True)
        for ps in self.chain[1:]:
            stub = bookstore_pb2_grpc.BookStoreStub(grpc.insecure_channel(ps))
            try:
                stub.ReadOperation(bookstore_pb2.ReadOperationRequest(book_name=request.book_name), timeout=10)
                stub.WriteOperation(bookstore_pb2.WriteOperationRequest(book_name=request.book_name, price=request.price), timeout=10)
            except Exception as e:
                print(f"Error propagating update to {ps}: {e}")
        return bookstore_pb2.WriteOperationResponse(book_name=request.book_name, price=request.price)

    def ListBooks(self, request, context):
        if not self.chain:
            return bookstore_pb2.ListBooksResponse()
        books = [bookstore_pb2.Book(name=name, price=price) for name, (price, _) in self.data[self.chain[0]].items()]
        print(books)
        return bookstore_pb2.ListBooksResponse(books=books)

    def ReadOperation(self, request, context):
        if not self.chain:
            return bookstore_pb2.ReadOperationResponse(price=0)
        current_ps = self.chain[0]
        for ps in self.chain:
            if self.data[ps].get("head"):
                current_ps = ps
                break
        if request.book_name in self.data[current_ps]:
            return bookstore_pb2.ReadOperationResponse(price=self.data[current_ps][request.book_name][0])
        for ps in self.chain[1:]:
            stub = bookstore_pb2_grpc.BookStoreStub(grpc.insecure_channel(ps))
            try:
                response = stub.ReadOperation(request, timeout=10)
                if response.price > 0:
                    return response
            except Exception as e:
                print(f"Error getting price from {ps}: {e}")
        return bookstore_pb2.ReadOperationResponse(price=0)

    def SetTimeout(self, request, context):
        # TODO: Implement SetTimeout
        return bookstore_pb2.SetTimeoutResponse(message="Timeout set successfully")

    def DataStatus(self, request, context):
        if not self.chain:
            return bookstore_pb2.DataStatusResponse()
        data_items = []
        for ps in self.chain:
            for name, (price, is_dirty) in self.data[ps].items():
                data_items.append(bookstore_pb2.DataItemStatus(name=name, is_dirty=is_dirty))
        return bookstore_pb2.DataStatusResponse(data_items=data_items)

    def RemoveHead(self, request, context):
        if not self.chain:
            return bookstore_pb2.RemoveHeadResponse(chain="")
        if len(self.chain) == 1:
            self.chain = []
        else:
            new_head = self.data[self.chain[0]]["successor"]
            del self.data[self.chain[0]]["head"]
            self.data[new_head]["predecessor"] = None
            self.chain.pop(0)
            self.chain[0] = new_head
        return bookstore_pb2.RemoveHeadResponse(chain=self.ListChain(bookstore_pb2.ListChainRequest(), context).chain)

    def RestoreHead(self, request, context):
        # TODO: Implement RestoreHead
        return bookstore_pb2.RestoreHeadResponse(message="Head restored successfully")

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreService(), server)
    server.add_insecure_port("[::]:50055")
    server.start()
    print("bookstore server started on port 50055...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
   
